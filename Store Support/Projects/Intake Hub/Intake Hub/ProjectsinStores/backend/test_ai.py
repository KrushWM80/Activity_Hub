import traceback
from ai_agent import AIAgent
import asyncio

agent = AIAgent()
try:
    result = asyncio.run(agent.process_query(
        'I would like to see GMD projects', 
        {
            'total_projects': 100, 
            'all_projects': [
                {'project_id': '1', 'title': 'Test GMD Project', 'division': 'EAST'}
            ]
        }
    ))
    print('SUCCESS:', result)
except Exception as e:
    print('ERROR:', e)
    traceback.print_exc()
