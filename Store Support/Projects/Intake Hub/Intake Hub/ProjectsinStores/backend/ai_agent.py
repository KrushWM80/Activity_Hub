import os
import json
from typing import Dict, Optional, List
import openai
from openai import AsyncOpenAI

class AIAgent:
    """Enhanced AI Agent for natural language queries about project data with improved search and question answering"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        
        if self.endpoint:
            # Azure OpenAI
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                azure_endpoint=self.endpoint
            )
        elif self.api_key:
            # OpenAI
            self.client = AsyncOpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def _search_owner_in_database(self, owner_name: str) -> List[Dict]:
        """
        Search for an owner's projects directly in BigQuery, bypassing normal filters.
        This finds projects that may be filtered out due to missing store numbers or inactive status.
        """
        try:
            from google.cloud import bigquery
            client = bigquery.Client(project='wmt-assetprotection-prod')
            
            # Search for owner in database without the usual filters
            query = f"""
                SELECT DISTINCT
                    COALESCE(Owner, PROJECT_OWNER, '') as owner,
                    COALESCE(PROJECT_TITLE, Title, 'Untitled') as title,
                    Project_Source as project_source,
                    COALESCE(Status, PROJECT_HEALTH, '') as status,
                    Division as division,
                    CAST(COALESCE(Facility, 0) AS STRING) as store,
                    COALESCE(PROJECT_PHASE_2, Phase, '') as phase
                FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
                WHERE (Owner IS NOT NULL AND Owner != '' AND LOWER(Owner) LIKE '%{owner_name.lower()}%')
                   OR (PROJECT_OWNER IS NOT NULL AND PROJECT_OWNER != '' AND LOWER(PROJECT_OWNER) LIKE '%{owner_name.lower()}%')
                LIMIT 50
            """
            
            result = client.query(query)
            projects = []
            for row in result:
                projects.append({
                    'owner': row.owner,
                    'title': row.title,
                    'project_source': row.project_source,
                    'status': row.status,
                    'division': row.division or 'N/A',
                    'store': row.store if row.store and row.store != '0' else None,
                    'phase': row.phase or 'N/A'
                })
            return projects
        except Exception as e:
            print(f"[DEBUG] Owner database search failed: {e}")
            return []
    
    async def process_query(self, query: str, context: Optional[Dict] = None) -> Dict:
        """Process natural language query about project data"""
        
        # Extract project list from context if available
        all_projects = context.get('all_projects', []) if context else []
        
        # Debug: Log how many projects we received
        print(f"[AI AGENT] Received query: '{query}'")
        print(f"[AI AGENT] Context has {len(all_projects)} projects")
        if all_projects and len(all_projects) > 0:
            sample = all_projects[0]
            print(f"[AI AGENT] Sample project keys: {list(sample.keys()) if isinstance(sample, dict) else 'not a dict'}")
            if isinstance(sample, dict):
                print(f"[AI AGENT] Sample owner value: '{sample.get('owner', 'NO OWNER KEY')}' / '{sample.get('Owner', 'NO Owner KEY')}'")
        
        if not self.client:
            return self._get_mock_response(query, context, all_projects)
        
        try:
            # Build system prompt with context
            system_prompt = self._build_system_prompt(context)
            
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "data": None
            }
            
        except Exception as e:
            return {
                "answer": f"I encountered an error: {str(e)}",
                "data": None
            }
    
    def _build_system_prompt(self, context: Optional[Dict]) -> str:
        """Build system prompt with context for AI"""
        base_prompt = """You are an AI assistant helping users explore project data from BigQuery. 
        You have access to information about projects, stores, divisions, and phases.
        Provide helpful, concise answers to user queries. If asked to find a project, search by name."""
        
        if context:
            base_prompt += f"\n\nCurrent context: {json.dumps(context, indent=2)}"
        
        return base_prompt
    
    def _extract_context(self, context: Optional[Dict]) -> Dict:
        """Extract relevant context for response"""
        if not context:
            return {}
        
        return {
            "total_projects": context.get("total_projects"),
            "visible_projects": context.get("project_count")
        }
    
    def _extract_filters_from_query(self, query: str, all_projects: list) -> dict:
        """Extract all possible filters from query: project names, phase, owner, week, region, market, etc.
        Returns: {
            'project_keywords': ['GMD'],
            'phase': 'POC/POT',
            'wm_week': 'WK52',
            'owner': 'Mike',
            'region': 'NE',
            'market': '208',
            'store_number': '5147',
            'found_projects': [...],
        }
        """
        filters = {
            'project_keywords': [],
            'phase': None,
            'wm_week': None,
            'owner': None,
            'region': None,
            'market': None,
            'store_number': None,
            'found_projects': []
        }
        
        query_lower = query.lower()
        query_clean = query.strip()
        import re
        
        # 0. Extract Store Number filter FIRST (4-digit numbers that could be store numbers)
        # Pattern: "store 5147", "#5147", or standalone 4-digit number like "5147"
        store_pattern = r'\b(?:store\s*#?|#)?(\d{4})\b'
        store_match = re.search(store_pattern, query_lower)
        if store_match:
            potential_store = store_match.group(1)
            # Verify it's a reasonable store number (typically 1-9999)
            if 1 <= int(potential_store) <= 9999:
                filters['store_number'] = potential_store
        
        # 1. Extract Region filter (e.g., "in region NE" or "region NE")
        region_pattern = r'(?:in\s+)?region\s+([A-Z]{1,2})'
        region_match = re.search(region_pattern, query_clean, re.IGNORECASE)
        if region_match:
            filters['region'] = region_match.group(1).upper()
        
        # 2. Extract Market filter (e.g., "in market 208" or "market 208")
        # Must have "market" followed by a number, NOT "market scale"
        market_pattern = r'(?:in\s+)?market\s+(\d+)'
        market_match = re.search(market_pattern, query_lower)
        if market_match:
            filters['market'] = market_match.group(1)
        
        # 3. Extract Phase filter (more carefully now)
        # Only recognize specific phase keywords, not generic "market"
        phase_map = {
            'pending': 'Pending',
            'poc': 'POC/POT',
            'pot': 'POC/POT',
            'test': 'Test',
            'mkt scale': 'Mkt Scale',  # Requires BOTH words
            'mkt-scale': 'Mkt Scale',
            'market scale': 'Mkt Scale',  # Requires BOTH words
            'roll': 'Roll/Deploy',
            'deploy': 'Roll/Deploy',
            'rollout': 'Roll/Deploy',
            'complete': 'Complete',
            'completed': 'Complete',
            'realty': 'Realty'  # Realty is also a Source, but kept here for Phase filter compatibility
        }
        for key, phase_name in phase_map.items():
            if key in query_lower:
                filters['phase'] = phase_name
                break
        
        # 2. Extract WM Week filter (wk 1-53, w1-53, week 1-53)
        import re
        wk_pattern = r'w(?:k|eek)?\s*(\d{1,2})'
        wk_match = re.search(wk_pattern, query_lower)
        if wk_match:
            week_num = wk_match.group(1).zfill(2)
            filters['wm_week'] = f"WK{week_num}"
        
        # 3. Extract Owner filter - look for owner names in various patterns
        import re
        # Pattern 1: "owner is [name]", "owner: [name]", "owned by [name]"
        owner_pattern = r'(?:owner\s+(?:is|:)?|owned\s+by)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
        owner_match = re.search(owner_pattern, query_clean, re.IGNORECASE)
        if owner_match:
            potential_owner = owner_match.group(1).strip()
            # Verify this looks like a real name (has reasonable length and not a keyword)
            if len(potential_owner) > 2 and potential_owner.lower() not in ['projects', 'project', 'data', 'admin']:
                filters['owner'] = potential_owner
                print(f"[DEBUG] Owner extracted via Pattern 1: '{filters['owner']}'")
        
        # Pattern 2: If no match yet, try to find capitalized names after "by"
        if not filters['owner']:
            by_pattern = r'\bby\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
            by_match = re.search(by_pattern, query_clean)
            if by_match:
                filters['owner'] = by_match.group(1).strip()
        
        # Pattern 3: If still no match, look for standalone capitalized names that might be owners
        if not filters['owner']:
            words = query_clean.split()
            for word in words:
                clean_word = word.strip('?,!.')
                # Check if it looks like a name (starts with capital, reasonable length)
                if (clean_word and clean_word[0].isupper() and 2 < len(clean_word) < 20 and
                    clean_word.lower() not in ['owner', 'project', 'projects', 'phase', 'wk', 'week',
                                               'poc', 'pot', 'test', 'mkt', 'scale', 'roll', 'deploy',
                                               'complete', 'realty', 'pending', 'i', 'the', 'a', 'do',
                                               'gmd', 'sidekick', 'vizpick', 'dsd', 'show', 'find', 'owned',
                                               'looking', 'projects', 'for', 'am', 'looking', 'owned']):
                    # Check if this might be an owner name by seeing if it appears in any Owner field
                    for project in all_projects:
                        project_owner = project.get('Owner') or project.get('owner') or project.get('PROJECT_OWNER') or ''
                        if project_owner and clean_word.lower() in project_owner.lower():
                            filters['owner'] = clean_word
                            break
                    if filters['owner']:
                        break
        
        # Pattern 4: Check for Intake Card numbers (numeric values)
        import re
        # Look for numeric patterns like "17902" or "card 17902" or "intake 17902"
        intake_pattern = r'(?:intake\s+)?(?:card\s+)?#?(\d{4,6})'
        intake_match = re.search(intake_pattern, query_clean, re.IGNORECASE)
        if intake_match and not filters['owner']:
            intake_card = intake_match.group(1)
            # Only treat as intake card if it's 5-6 digits (not store number length)
            if len(intake_card) >= 5:
                # Try to find project with this intake card
                for project in all_projects:
                    if str(project.get('Intake_Card', '')) == intake_card:
                        filters['owner'] = intake_card  # Store as identifier
                        break
        
        # 4. Extract project keywords (meaningful words, not stop words)
        # NOTE: Keep searchable terms like "remodel", "expansion", "refresh" etc.
        stop_words = {
            'do', 'you', 'see', 'have', 'any', 'the', 'a', 'an', 'and', 'or', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'has', 'had', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'show', 'find', 'get', 'list',
            'display', 'what', 'which', 'where', 'when', 'why', 'how', 'tell', 'give', 'provide',
            'search', 'looking', 'for', 'with', 'in', 'of', 'on', 'at', 'by', 'from', 'to',
            'up', 'down', 'about', 'out', 'all', 'each', 'every', 'both', 'as', 'if', 'than',
            'that', 'this', 'these', 'those', 'me', 'my', 'we', 'us', 'our', 'them', 'their',
            'projects', 'project', 'data', 'info', 'information', 'detail', 'details', 'please',
            'thanks', 'thank', 'i', 'im', "i'm", 'want', 'like', 'need', 'know', 'think',
            'just', 'now', 'it', 'its', 'there', 'here', 'ok', 'yes', 'no', 'phase', 'week',
            'owner', 'wk', 'w', 'poc', 'pot', 'test', 'mkt', 'scale', 'roll', 'deploy',
            'rollout', 'complete', 'pending', 'store', 'stores'
        }
        # Note: Removed 'realty' from stop words since it's a valid search term for Realty projects
        
        query_words = query_lower.split()
        # Exclude the store number from keywords if already captured
        store_num = filters.get('store_number')
        meaningful_words = [w.strip('?,!.') for w in query_words 
                          if w.strip('?,!.') not in stop_words 
                          and len(w.strip('?,!.')) >= 2
                          and w.strip('?,!.') != store_num]
        
        # Search for meaningful words in project titles
        found_projects = []
        for project in all_projects:
            title = project.get('title', '').lower()
            for keyword in meaningful_words:
                if keyword in title:
                    found_projects.append(project)
                    # Only add keyword once to avoid duplicates
                    if keyword not in filters['project_keywords']:
                        filters['project_keywords'].append(keyword)
                    break
        
        filters['found_projects'] = found_projects
        return filters

    def _get_mock_response(self, query: str, context: Optional[Dict] = None, all_projects: list = []) -> Dict:
        """Enhanced AI response with better search, data analysis, and question answering"""
        query_lower = query.lower()
        query_clean = query.strip()
        
        # PRIORITY 1: Extract all filters from query
        filter_info = self._extract_filters_from_query(query_clean, all_projects)
        
        # Build response based on what was found
        extracted_projects = filter_info['found_projects']
        phase_filter = filter_info['phase']
        wm_week_filter = filter_info['wm_week']
        owner_filter = filter_info['owner']
        region_filter = filter_info['region']
        market_filter = filter_info['market']
        store_filter = filter_info.get('store_number')
        project_keywords = filter_info['project_keywords']
        
        # If no keyword matches but we have filter criteria, start with ALL projects
        # This allows owner-only, region-only, market-only, store-only, etc. searches to work
        if not extracted_projects and (owner_filter or region_filter or market_filter or phase_filter or wm_week_filter or store_filter):
            extracted_projects = all_projects
            print(f"[DEBUG] No keywords found, using all_projects. Store filter: '{store_filter}', Keywords: {project_keywords}")
        
        # Apply additional filters to the found projects
        if extracted_projects:
            # Filter by store number if specified
            if store_filter:
                print(f"[DEBUG] Filtering by store: '{store_filter}'")
                print(f"[DEBUG] Projects before store filter: {len(extracted_projects)}")
                extracted_projects = [p for p in extracted_projects 
                                     if str(p.get('store', '')) == store_filter or str(p.get('store_number', '')) == store_filter]
                print(f"[DEBUG] Projects after store filter: {len(extracted_projects)}")
            
            # Filter by phase if specified
            if phase_filter:
                extracted_projects = [p for p in extracted_projects if p.get('phase') == phase_filter]
            
            # Filter by WM Week if specified
            if wm_week_filter:
                extracted_projects = [p for p in extracted_projects if p.get('wm_week') == wm_week_filter]
            
            # Filter by owner if specified (search in OWNER column)
            if owner_filter:
                print(f"[DEBUG] Filtering by owner: '{owner_filter}'")
                print(f"[DEBUG] Projects before owner filter: {len(extracted_projects)}")
                extracted_projects = [p for p in extracted_projects 
                                     if owner_filter.lower() in (p.get('Owner') or p.get('owner') or p.get('PROJECT_OWNER') or '').lower()]
                print(f"[DEBUG] Projects after owner filter: {len(extracted_projects)}")
                if len(extracted_projects) == 0:
                    # Debug: show some owner values from original projects
                    print(f"[DEBUG] Sample Owner values from database:")
                    for p in all_projects[:5]:
                        print(f"  - {p.get('Owner') or p.get('owner') or p.get('PROJECT_OWNER') or 'NULL'}")
            
            # Filter by region if specified
            if region_filter:
                extracted_projects = [p for p in extracted_projects if p.get('region') == region_filter]
            
            # Filter by market if specified
            if market_filter:
                extracted_projects = [p for p in extracted_projects if str(p.get('market', '')).strip() == market_filter]
        
        # If found projects, return them
        if extracted_projects:
            unique_titles = sorted(list(set([p.get('title', '') for p in extracted_projects])))
            store_count = len(extracted_projects)
            
            project_list = '\n'.join([f"• {title}" for title in unique_titles[:10]])
            if len(unique_titles) > 10:
                project_list += f"\n• ...and {len(unique_titles) - 10} more"
            
            # Build filter string for display
            filter_parts = []
            if project_keywords:
                # Limit keywords shown to prevent overwhelming output
                displayed_keywords = ' '.join(sorted(project_keywords)[:5]).upper()
                if len(project_keywords) > 5:
                    displayed_keywords += f" (+{len(project_keywords) - 5} more)"
                filter_parts.append(displayed_keywords)
            if store_filter:
                filter_parts.append(f"Store {store_filter}")
            if phase_filter:
                filter_parts.append(f"{phase_filter} Phase")
            if region_filter:
                filter_parts.append(f"Region {region_filter}")
            if market_filter:
                filter_parts.append(f"Market {market_filter}")
            if wm_week_filter:
                filter_parts.append(f"{wm_week_filter}")
            if owner_filter:
                filter_parts.append(f"Owner: {owner_filter}")
            
            filter_display = ' + '.join(filter_parts) if filter_parts else query_clean
            
            # Build response message
            response_msg = f"🔍 **Found {len(unique_titles)} projects matching '{filter_display}':**\n\n{project_list}\n\n📊 **Total:** {store_count} stores across these projects"
            
            if phase_filter or wm_week_filter or owner_filter or region_filter or market_filter or store_filter:
                response_msg += "\n\n🎯 Applied filters:"
                if project_keywords:
                    response_msg += f"\n  • Project: {' '.join(sorted(project_keywords)).upper()}"
                if store_filter:
                    response_msg += f"\n  • Store: {store_filter}"
                if region_filter:
                    response_msg += f"\n  • Region: {region_filter}"
                if market_filter:
                    response_msg += f"\n  • Market: {market_filter}"
                if phase_filter:
                    response_msg += f"\n  • Phase: {phase_filter}"
                if wm_week_filter:
                    response_msg += f"\n  • WM Week: {wm_week_filter}"
                if owner_filter:
                    response_msg += f"\n  • Owner: {owner_filter}"
            
            response_msg += "\n\n💡 **Tip:** Type a specific project name for more details."
            
            return {
                "answer": response_msg,
                "data": {
                    "matching_projects": extracted_projects[:100],
                    "suggested_filter": ' '.join(sorted(project_keywords)) if project_keywords else None,
                    "store_filter": store_filter,
                    "phase_filter": phase_filter,
                    "wm_week_filter": wm_week_filter,
                    "region_filter": region_filter,
                    "market_filter": market_filter,
                    "owner_filter": owner_filter,
                    "total_count": store_count,
                    "unique_projects": len(unique_titles)
                }
            }
        
        # If we extracted a specific filter but found NO projects, return a message explaining why
        if owner_filter or phase_filter or wm_week_filter or region_filter or market_filter or project_keywords or store_filter:
            filter_parts = []
            if project_keywords:
                filter_parts.append(f"project '{' '.join(project_keywords)}'")
            if store_filter:
                filter_parts.append(f"store '{store_filter}'")
            if owner_filter:
                filter_parts.append(f"owner '{owner_filter}'")
            if phase_filter:
                filter_parts.append(f"phase '{phase_filter}'")
            if region_filter:
                filter_parts.append(f"region '{region_filter}'")
            if market_filter:
                filter_parts.append(f"market '{market_filter}'")
            if wm_week_filter:
                filter_parts.append(f"week '{wm_week_filter}'")
            
            filter_desc = ' + '.join(filter_parts)
            
            # SPECIAL CASE: If searching for a store + keyword combo but no results,
            # fall back to showing ALL projects for that store
            if store_filter and project_keywords and all_projects:
                # Try to find ANY projects for this store (ignoring keywords)
                store_projects = [p for p in all_projects 
                                 if str(p.get('store', '')) == store_filter or str(p.get('store_number', '')) == store_filter]
                if store_projects:
                    unique_titles = sorted(list(set([p.get('title', '') for p in store_projects])))
                    project_list = '\n'.join([f"• {title}" for title in unique_titles[:10]])
                    if len(unique_titles) > 10:
                        project_list += f"\n• ...and {len(unique_titles) - 10} more"
                    
                    keyword_str = ' '.join(project_keywords).upper()
                    return {
                        "answer": f"🔍 **No '{keyword_str}' projects found for Store {store_filter}**\n\nHowever, here's what we found for Store {store_filter}:\n\n{project_list}\n\n📊 **Total:** {len(unique_titles)} projects at this store\n\n🎯 Dashboard filtered to Store {store_filter}!",
                        "data": {
                            "matching_projects": store_projects[:100],
                            "suggested_filter": None,
                            "store_filter": store_filter,
                            "total_count": len(store_projects),
                            "unique_projects": len(unique_titles)
                        }
                    }
            
            # SPECIAL CASE: If searching for a store only but no results
            if store_filter and not project_keywords and all_projects:
                return {
                    "answer": f"❌ **No projects found** for Store {store_filter}.\n\nThis store may not have any active projects currently, or the data may not include this store number.\n\n💡 **Try:** Searching for a project name, or check if the store number is correct.",
                    "data": {
                        "matching_projects": [],
                        "suggested_filter": None,
                        "store_filter": store_filter,
                        "total_count": 0,
                        "unique_projects": 0
                    }
                }
            
            # SPECIAL CASE: If searching by owner and no results, check if they have projects that are filtered out
            if owner_filter:
                try:
                    owner_projects = self._search_owner_in_database(owner_filter)
                    if owner_projects:
                        # Owner has projects but they're filtered out - explain why
                        projects_without_stores = [p for p in owner_projects if not p.get('store')]
                        inactive_projects = [p for p in owner_projects if p.get('status', '').lower() == 'inactive']
                        
                        # Build explanation message
                        project_titles = list(set([p.get('title', 'Untitled') for p in owner_projects]))
                        
                        reason_parts = []
                        if projects_without_stores:
                            reason_parts.append("don't have store assignments")
                        if inactive_projects:
                            reason_parts.append("are inactive")
                        
                        reason_text = " or ".join(reason_parts) if reason_parts else "are filtered from the main view"
                        
                        # Create a detailed response
                        project_list = "\n".join([f"• **{title}**" for title in project_titles[:10]])
                        if len(project_titles) > 10:
                            project_list += f"\n• ...and {len(project_titles) - 10} more"
                        
                        return {
                            "answer": f"📋 **{owner_filter}** owns {len(project_titles)} project(s), but they {reason_text}:\n\n{project_list}\n\n*These projects don't appear in the filtered view because they either lack store assignments or are marked inactive.*",
                            "data": {
                                "matching_projects": [],
                                "suggested_filter": None,
                                "phase_filter": phase_filter,
                                "wm_week_filter": wm_week_filter,
                                "region_filter": region_filter,
                                "market_filter": market_filter,
                                "owner_filter": owner_filter,
                                "total_count": 0,
                                "unique_projects": 0,
                                "filtered_out_projects": project_titles
                            }
                        }
                except Exception as e:
                    print(f"[DEBUG] Owner fallback search error: {e}")
            
            return {
                "answer": f"❌ **No projects found** matching {filter_desc}. Try adjusting your search or filters.",
                "data": {
                    "matching_projects": [],
                    "suggested_filter": None,
                    "store_filter": store_filter,
                    "phase_filter": phase_filter,
                    "wm_week_filter": wm_week_filter,
                    "region_filter": region_filter,
                    "market_filter": market_filter,
                    "owner_filter": owner_filter,
                    "total_count": 0,
                    "unique_projects": 0
                }
            }
        
        # First check if this is a pure QUESTION (not a project search with filters)
        # Questions should NEVER trigger a filter
        question_indicators = [
            "how many", "how much", "what", "when", "where", "why", "who",
            "can you", "could you", "would you", "tell me",
            "explain", "describe", "help"
        ]
        
        # "show me" is ambiguous - check if it has a project/division/phase keyword
        has_filter_keyword = any(kw in query_lower for kw in [
            'division', 'region', 'market', 'store', 'phase', 'week', 'wk',
            'gmd', 'sidekick', 'dsd', 'project', 'realty', 'operations', 'remodel'
        ])
        
        is_question = (
            query_clean.endswith('?') and not has_filter_keyword or
            any(indicator in query_lower for indicator in question_indicators) and not has_filter_keyword
        )
        
        # Get context statistics
        total_projects = context.get('total_projects', 0) if context else 0
        
        # If it's a question, skip project search and go to question answering
        if not is_question:
            # PRIORITY 1: Check for specific filter requests FIRST (Division, Region, Market, Store, Phase, Source)
            
            # Division filtering
            for division in ['EAST', 'WEST', 'NORTH', 'SOUTH', 'SOUTHEAST', 'SOUTHWEST', 'NHM', 'CENTRAL', 'NATIONAL']:
                if division.lower() in query_lower and ('show' in query_lower or 'projects' in query_lower or 'filter' in query_lower or 'division' in query_lower):
                    matching = [p for p in all_projects if p.get('division', '').upper() == division] if all_projects else []
                    unique_projects = len(set(p.get('project_id', '') for p in matching))
                    return {
                        "answer": f"📍 **Filtering to {division} Division**\n\n✅ Found {unique_projects} projects impacting {len(matching)} stores\n\n🎯 Dashboard filtered!\n\n💡 Would you like to narrow this down by WM WK?",
                        "data": {"matching_projects": matching[:100], "suggested_filter": None, "division_filter": division, "total_count": len(matching), "unique_projects": unique_projects}
                    }
            
            # Phase filtering
            phases_map = {'pending': 'Pending', 'poc': 'POC/POT', 'pot': 'POC/POT', 'test': 'Test', 
                         'market': 'Mkt Scale', 'mkt': 'Mkt Scale', 'scale': 'Mkt Scale',
                         'roll': 'Roll/Deploy', 'deploy': 'Roll/Deploy', 'rollout': 'Roll/Deploy',
                         'complete': 'Complete', 'completed': 'Complete', 'realty': 'Realty'}
            for key, phase_name in phases_map.items():
                if key in query_lower and ('show' in query_lower or 'projects' in query_lower or 'filter' in query_lower or 'phase' in query_lower):
                    matching = [p for p in all_projects if p.get('phase', '') == phase_name] if all_projects else []
                    unique_projects = len(set(p.get('project_id', '') for p in matching))
                    return {
                        "answer": f"🔄 **Filtering to {phase_name} Phase**\n\n✅ Found {unique_projects} projects impacting {len(matching)} stores\n\n🎯 Dashboard filtered!",
                        "data": {"matching_projects": matching[:100], "suggested_filter": None, "phase_filter": phase_name}
                    }
            
            # Source filtering with optional division combination
            # Check for division in the query
            divisions = {'east': 'EAST', 'west': 'WEST', 'north': 'NORTH', 'south': 'SOUTH', 'central': 'CENTRAL'}
            detected_division = None
            for div_key, div_value in divisions.items():
                if div_key in query_lower:
                    detected_division = div_value
                    break
            
            if 'operations' in query_lower and ('show' in query_lower or 'projects' in query_lower or 'filter' in query_lower or 'source' in query_lower or 'in' in query_lower):
                matching = [p for p in all_projects if p.get('project_source', '') == 'Operations'] if all_projects else []
                # Apply division filter if detected
                if detected_division:
                    matching = [p for p in matching if p.get('division', '').upper() == detected_division]
                unique_projects = len(set(p.get('project_id', '') for p in matching))
                filter_desc = "Operations Projects"
                if detected_division:
                    filter_desc += f" in {detected_division} Division"
                data_payload = {"matching_projects": matching[:100], "suggested_filter": None, "source_filter": "Operations"}
                if detected_division:
                    data_payload["division_filter"] = detected_division
                return {
                    "answer": f"📦 **Filtering to {filter_desc}**\n\n✅ Found {unique_projects} projects impacting {len(matching)} stores\n\n🎯 Dashboard filtered!",
                    "data": data_payload
                }
            if 'realty' in query_lower and ('show' in query_lower or 'projects' in query_lower or 'filter' in query_lower or 'source' in query_lower or 'in' in query_lower):
                matching = [p for p in all_projects if p.get('project_source', '') == 'Realty'] if all_projects else []
                # Apply division filter if detected
                if detected_division:
                    matching = [p for p in matching if p.get('division', '').upper() == detected_division]
                unique_projects = len(set(p.get('project_id', '') for p in matching))
                filter_desc = "Realty Projects"
                if detected_division:
                    filter_desc += f" in {detected_division} Division"
                data_payload = {"matching_projects": matching[:100], "suggested_filter": None, "source_filter": "Realty"}
                if detected_division:
                    data_payload["division_filter"] = detected_division
                return {
                    "answer": f"🏢 **Filtering to {filter_desc}**\n\n✅ Found {unique_projects} projects impacting {len(matching)} stores\n\n🎯 Dashboard filtered!",
                    "data": data_payload
                }
            
            # Region filtering - check for region patterns including numeric (Region 47, R47, etc)
            if all_projects:
                import re
                # Check for numeric region pattern: "region 47", "r47", "region47", "show me region 47"
                region_num_pattern = r'(?:region|r)\s*(\d+)'
                region_num_match = re.search(region_num_pattern, query_lower)
                if region_num_match and ('show' in query_lower or 'region' in query_lower or 'filter' in query_lower):
                    region_num = region_num_match.group(1)
                    # Try to find region containing this number
                    for p in all_projects:
                        region = p.get('region', '')
                        if region and region_num in str(region):
                            matching = [proj for proj in all_projects if proj.get('region', '') == region]
                            unique_projects = len(set(proj.get('project_id', '') for proj in matching))
                            return {
                                "answer": f"🗺️ **Filtering to {region}**\n\n✅ Found {unique_projects} projects impacting {len(matching)} stores\n\n🎯 Dashboard filtered!",
                                "data": {"matching_projects": matching[:100], "suggested_filter": None, "region_filter": region, "total_count": len(matching), "unique_projects": unique_projects}
                            }
                # Otherwise check for region name match
                elif 'region' in query_lower:
                    all_regions = set(p.get('region', '') for p in all_projects if p.get('region'))
                    for region in all_regions:
                        if region.lower() in query_lower and ('show' in query_lower or 'projects' in query_lower or 'filter' in query_lower):
                            matching = [p for p in all_projects if p.get('region', '') == region]
                            unique_projects = len(set(p.get('project_id', '') for p in matching))
                            return {
                                "answer": f"🗺️ **Filtering to {region}**\n\n✅ Found {unique_projects} projects impacting {len(matching)} stores\n\n🎯 Dashboard filtered!",
                                "data": {"matching_projects": matching[:100], "suggested_filter": None, "region_filter": region}
                            }
            
            # Market filtering
            if all_projects and 'market' in query_lower:
                all_markets = set(p.get('market', '') for p in all_projects if p.get('market'))
                for market in all_markets:
                    # Check if market name appears in query (case-insensitive)
                    market_words = market.lower().split()
                    if any(word in query_lower for word in market_words if len(word) > 3):
                        if 'show' in query_lower or 'projects' in query_lower or 'filter' in query_lower or 'market' in query_lower:
                            matching = [p for p in all_projects if p.get('market', '') == market]
                            unique_projects = len(set(p.get('project_id', '') for p in matching))
                            return {
                                "answer": f"📍 **Filtering to {market} Market**\n\n✅ Found {unique_projects} projects impacting {len(matching)} stores\n\n🎯 Dashboard filtered!",
                                "data": {"matching_projects": matching[:100], "suggested_filter": None, "market_filter": market}
                            }
            
            # Store filtering - check for store number patterns
            import re
            store_pattern = r'\b(?:store|#)\s*(\d{4})\b'
            store_match = re.search(store_pattern, query_lower)
            if store_match and all_projects:
                store_num = store_match.group(1)
                matching = [p for p in all_projects if str(p.get('store_number', '')) == store_num]
                unique_projects = len(set(p.get('project_id', '') for p in matching))
                return {
                    "answer": f"🏪 **Filtering to Store {store_num}**\n\n✅ Found {unique_projects} projects\n\n🎯 Dashboard filtered!",
                    "data": {"matching_projects": matching[:100], "suggested_filter": None, "store_filter": store_num}
                }
            
            # PRIORITY 2: Check for WM Week filtering
            import re
            wm_week_pattern = r'w[ek]{1,2}\s*(\d{1,2})'
            wm_week_match = re.search(wm_week_pattern, query_lower)
            if wm_week_match:
                week_num = wm_week_match.group(1).zfill(2)  # Pad to 2 digits
                wm_week = f"WK{week_num}"
                
                # Check if query also mentions a project name
                project_keywords = []
                for term in query_lower.split():
                    if term not in ['how', 'many', 'projects', 'for', 'in', 'wk', 'week', week_num, 'the', 'a', 'an', '?']:
                        project_keywords.append(term)
                
                if all_projects:
                    # Filter by WM Week
                    week_projects = [p for p in all_projects if p.get('wm_week') == wm_week]
                    
                    # If project keywords mentioned, further filter
                    if project_keywords:
                        keyword_str = ' '.join(project_keywords)
                        week_projects = [p for p in week_projects 
                                       if any(kw in p.get('title', '').lower() for kw in project_keywords)]
                        return {
                            "answer": f"📅 **{keyword_str.upper()} Projects in {wm_week}**\n\n✅ Found {len(week_projects)} projects\n\n🎯 Filtering dashboard now!",
                            "data": {
                                "matching_projects": week_projects,
                                "suggested_filter": keyword_str,
                                "wm_week_filter": wm_week
                            }
                        }
                    else:
                        return {
                            "answer": f"📅 **Projects in {wm_week}**\n\n✅ Found {len(week_projects)} projects\n\n🎯 Filtering dashboard now!",
                            "data": {
                                "matching_projects": week_projects,
                                "suggested_filter": None,
                                "wm_week_filter": wm_week
                            }
                        }
            
            # PRIORITY 3: Check for exact project title match (user typed exact name)
            exact_match = None
            if all_projects:
                for project in all_projects:
                    if project.get('title', '').lower() == query_clean.lower():
                        exact_match = project
                        break
            
            if exact_match:
                # Found exact match - filter to this project only
                return {
                    "answer": f"✅ **Found exact match: {exact_match['title']}**\n\n📊 **Details:**\n• Project ID: {exact_match.get('project_id', 'N/A')}\n• Division: {exact_match.get('division', 'N/A')}\n• Phase: {exact_match.get('phase', 'N/A')}\n\n🎯 Filtering dashboard to show this project!",
                    "data": {
                        "matching_projects": [exact_match],
                        "suggested_filter": exact_match['title']
                    }
                }
            
            # PRIORITY 4: General project title search
            matching_projects = []
            if all_projects:
                # Extract meaningful search terms from query
                # Remove common filler words and focus on key terms
                filler_words = {
                    'want', 'to', 'see', 'show', 'me', 'find', 'get', 'the', 'a', 'an', 'is', 'are', 
                    'project', 'projects', 'all', 'i', "i'd", 'would', 'like', 'please', 'can', 'you',
                    'tell', 'give', 'list', 'display', 'for', 'with', 'in', 'of', 'on', 'at',
                    'by', 'from', 'as', 'what', 'which', 'there', 'their', 'they', 'that', 'this'
                }
                search_terms = [term for term in query_lower.split() if term not in filler_words and len(term) >= 2]
                
                # Strategy 1: Search for each meaningful term in project titles
                if search_terms:
                    for project in all_projects:
                        title_lower = project.get('title', '').lower()
                        # Match if ANY meaningful search term is found in title
                        if any(term in title_lower for term in search_terms):
                            matching_projects.append(project)
                
                # Strategy 2: Fallback to exact phrase if no terms extracted
                if not matching_projects and not search_terms:
                    for project in all_projects:
                        title = project.get('title', '')
                        if query_clean.lower() in title.lower():
                            matching_projects.append(project)
            
            # Handle project search results
            if matching_projects:
                # Get ALL unique titles, not just first 100
                unique_titles = list(set([p.get('title', '') for p in matching_projects]))
                unique_titles.sort()  # Alphabetical order
                
                # Only auto-apply if EXACTLY 1 unique project found AND query looks like an exact title
                # Don't auto-apply for keyword searches like "GMD"
                is_exact_match = len(unique_titles) == 1 or (
                    query_clean.lower() in [t.lower() for t in unique_titles]
                )
                
                if len(unique_titles) == 1 and is_exact_match:
                    project_title = unique_titles[0]
                    store_count = len(matching_projects)
                    
                    # Get additional context about the project
                    sample_project = matching_projects[0]
                    division = sample_project.get('division', 'Unknown')
                    phase = sample_project.get('phase', 'Unknown')
                    
                    return {
                        "answer": f"🎯 **Found: {project_title}**\n\n📊 **Details:**\n• Stores: {store_count}\n• Division: {division}\n• Phase: {phase}\n\n✅ Filtering dashboard to show this project now!",
                        "data": {
                            "matching_projects": matching_projects[:10],
                            "suggested_filter": project_title
                        }
                    }
                else:
                    # Multiple projects found - show them all
                    project_list = '\n'.join([f"• {title}" for i, title in enumerate(unique_titles[:10])])
                    if len(unique_titles) > 10:
                        project_list += f"\n• ...and {len(unique_titles) - 10} more"
                    
                    # Smart filter term selection: prefer the term that appears in the most project titles
                    if search_terms:
                        term_scores = {}
                        for term in search_terms:
                            # Count how many unique titles contain this term
                            score = sum(1 for title in unique_titles if term in title.lower())
                            term_scores[term] = score
                        # Pick the term with highest score (most matches)
                        filter_term = max(term_scores, key=term_scores.get)
                    else:
                        filter_term = query.lower()
                    
                    store_count = len(matching_projects)
                    
                    return {
                        "answer": f"🔍 **Found {len(unique_titles)} projects matching '{query}':**\n\n{project_list}\n\n📊 **Total:** {store_count} stores across these projects\n\n🎯 Dashboard is now filtered to these results!\n\n💡 **Tip:** Type a specific project name for more details.",
                        "data": {
                            "matching_projects": matching_projects[:100],
                            "suggested_filter": filter_term
                        }
                    }
        
        # Enhanced question answering - more comprehensive responses
        
        # Statistics/summary requests
        if any(phrase in query_lower for phrase in ["summary", "stats", "statistics", "overview", "breakdown", "give me a summary", "summarize"]):
            if all_projects:
                # Calculate statistics
                unique_projects = len(set(p.get('title', '') for p in all_projects))
                divisions = {}
                phases = {}
                for p in all_projects:
                    div = p.get('division', 'Unknown')
                    phase = p.get('phase', 'Unknown')
                    divisions[div] = divisions.get(div, 0) + 1
                    phases[phase] = phases.get(phase, 0) + 1
                
                # Sort by count descending
                top_divisions = sorted(divisions.items(), key=lambda x: x[1], reverse=True)[:5]
                top_phases = sorted(phases.items(), key=lambda x: x[1], reverse=True)[:5]
                
                div_breakdown = '\n'.join([f"  • {d}: {c} stores" for d, c in top_divisions])
                phase_breakdown = '\n'.join([f"  • {p}: {c} stores" for p, c in top_phases])
                
                return {
                    "answer": f"📊 **Dashboard Summary**\n\n📈 **Total:** {unique_projects} unique projects across {len(all_projects)} store assignments\n\n🌎 **Top Divisions:**\n{div_breakdown}\n\n🔄 **By Phase:**\n{phase_breakdown}\n\n💡 **Try:** 'Show me EAST division' or 'Projects in POC phase'",
                    "data": None
                }
        
        # Project count questions
        if any(phrase in query_lower for phrase in ["how many project", "total project", "count project", "number of project"]):
            # Calculate actual unique project count if we have data
            actual_count = total_projects
            if all_projects:
                actual_count = len(set(p.get('title', '') for p in all_projects))
            return {
                "answer": f"📊 **Total Projects: {actual_count}**\n\nI can break this down by:\n• **Division** - Geographic regions (EAST, WEST, NORTH, etc.)\n• **Phase** - Project stage (Roll/Deploy, Test, Complete, etc.)\n• **Store Count** - Projects per store\n\n💡 **Try asking:** 'Show me EAST division projects' or 'What phases are available?'",
                "data": None
            }
        
        # Store count questions
        if any(phrase in query_lower for phrase in ["how many store", "total store", "count store", "number of store"]):
            return {
                "answer": f"🏬 **Store-Level Data:**\n\nThis dashboard shows project assignments at the store level. Each row represents one project at one specific store.\n\n📍 **Navigation Options:**\n1. Use filters (Division, Region, Market)\n2. Click hierarchical navigation buttons\n3. Export CSV for detailed analysis\n\n💡 **Try:** Click on a Division button to see regional breakdown!",
                "data": None
            }
        
        # Division questions
        if "division" in query_lower:
            divisions = ['EAST', 'WEST', 'NORTH', 'SOUTHEAST', 'SOUTHWEST', 'NHM']
            return {
                "answer": f"📍 **Geographic Divisions:**\n\n{chr(10).join([f'• **{div}**' for div in divisions])}\n\n🎯 **What you can do:**\n1. Use the Division filter dropdown\n2. Click Division navigation buttons\n3. Drill down: Division → Region → Market → Store\n\n💡 **Try asking:** 'Show me EAST division' or 'What's in WEST?'",
                "data": None
            }
        
        # Phase questions
        if "phase" in query_lower or "stage" in query_lower:
            phases = [
                "**Roll/Deploy** - Active rollout to stores",
                "**Test** - Testing and validation phase",
                "**Mkt Scale** - Market scaling operations",
                "**POC/POT** - Proof of concept/technology",
                "**Complete** - Project finished",
                "**Pending** - Awaiting next action"
            ]
            return {
                "answer": f"🔄 **Project Phases:**\n\n{chr(10).join([f'• {p}' for p in phases])}\n\n🎯 Use the Phase filter dropdown to see projects in each stage!\n\n💡 **Try:** 'Show me Roll/Deploy projects' or 'What's in testing?'",
                "data": None
            }
        
        # Export questions
        if any(phrase in query_lower for phrase in ["export", "download", "csv", "excel"]):
            return {
                "answer": "📥 **Export Data to CSV:**\n\n1. Click the **'📥 Export to CSV'** button at the top\n2. Your filtered data will download immediately\n3. Includes: Project ID, Title, Division, Region, Market, Store Number, Phase, and more!\n\n✨ **Pro tip:** Apply filters first, then export to get exactly the data you need!",
                "data": None
            }
        
        # Filter/search help
        if any(phrase in query_lower for phrase in ["how to filter", "how to search", "how do i find"]):
            return {
                "answer": "🔍 **How to Find Projects:**\n\n**Method 1: Ask me directly**\n• Just type the project name (e.g., 'Sidekick', 'GMD')\n\n**Method 2: Use filters**\n• Division, Region, Market, Phase, Tribe, Store, WM Week\n\n**Method 3: Navigate hierarchically**\n• Click Division → Region → Market → Store buttons\n\n💡 I'll help you find anything - just ask!",
                "data": None
            }
        
        # Help command - more comprehensive
        if "help" in query_lower or "what can" in query_lower or "capabilities" in query_lower or query_lower.strip() in ['hi', 'hello', 'hey', '?']:
            return {
                "answer": "👋 **I'm Sparky - Your Project Data Assistant!**\n\n🔍 **Here's what I can help you with:**\n\n**📦 Find Projects**\n• Search by name: `Sidekick`, `GMD`, `DSD`, `VizPick`\n• Filter by owner: `projects owned by Mike`\n• Filter by intake card: `intake card 17902`\n\n**📍 Filter by Location**\n• `Show me EAST division`\n• `Projects in region NE`\n• `Market 208 projects`\n• `Store 1234`\n\n**🔄 Filter by Phase**\n• `POC projects`, `Roll/Deploy`, `Test phase`\n• `What's in Mkt Scale?`\n\n**📅 Filter by Time**\n• `Projects in WK52`, `Week 3`\n\n**📊 Get Stats**\n• `Give me a summary`\n• `How many projects?`\n• `Statistics overview`\n\n**🔗 Combine Filters**\n• `GMD projects in POC phase`\n• `Projects owned by Mike in EAST`\n• `Sidekick in WK52`\n\n💡 **Just type naturally - I understand!**",
                "data": None
            }
        
        # Default response - helpful and encouraging
        return {
            "answer": f"👋 **Hi! I'm Sparky!**\n\n📊 I have access to **{total_projects} active projects** across thousands of stores in BigQuery.\n\n🎯 **Quick actions:**\n• **Search projects:** Just type a project name (e.g., `GMD`, `Sidekick`)\n• **Search by owner:** `projects owned by Mike` or `owner: John`\n• **Get stats:** Type `summary` or `statistics`\n• **Get help:** Type `help` for full command list\n\n💡 **Example queries:**\n• `Show me Sidekick projects`\n• `POC projects in EAST`\n• `Projects owned by Mike`\n• `Give me a summary`\n\nWhat would you like to explore?",
            "data": None
        }
