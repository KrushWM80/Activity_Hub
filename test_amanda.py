from Interface.send_projects_owner_emails import query_owner_projects, generate_owner_email_html
from pathlib import Path

owner = 'Amanda Falkowski'
projects = query_owner_projects(owner, include_only_not_updated=False)

if projects:
    print(f'Found {len(projects)} projects for {owner}:')
    for p in projects:
        print(f"  - {p['title']} (Health: {p['health']}, Updated: {p['updated']}, Notes: {p['project_update']})")
    
    html = generate_owner_email_html(owner, projects, 'monday')
    
    # Save demo
    demo_file = Path('Interface/test_email_amanda.html')
    demo_file.write_text(html, encoding='utf-8')
    print(f'\n✓ Test email saved to: {demo_file}')
    print(f'  Projects: {len(projects)}')
    print(f'  Size: {len(html):,} bytes')
else:
    print(f'No projects found for {owner}')
