"""Optional link availability check. Manual content review remains separate."""
import concurrent.futures
import json
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parent.parent
bank=json.loads((ROOT/'data/questions.json').read_text(encoding='utf-8'))
references={r['url']:r['title'] for q in bank['questions'] if q.get('clarification') for r in q['clarification']['references']}

def check(pair):
    url,title=pair
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'ResearchReviewer-LinkCheck/1.0'})
        with urllib.request.urlopen(request,timeout=20) as response:
            return {'title':title,'url':url,'httpStatus':response.status,'finalUrl':response.url}
    except Exception as error:
        return {'title':title,'url':url,'error':str(error)}

with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
    results=list(pool.map(check,references.items()))
record={'checkedOn':datetime.now(ZoneInfo('Asia/Manila')).date().isoformat(),
        'note':'HTTP availability is separate from manual semantic review. Some publishers reject command-line clients while remaining readable in the browser/search retrieval tool. See VALIDATION.md for the distinction.',
        'references':results}
(ROOT/'audit/reference-checks.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
for result in results:print(result['title']+': '+str(result.get('httpStatus',result.get('error'))))
