import json
import os
import tempfile
import unittest
from io import BytesIO
from unittest.mock import patch
from agent import Memory, TOOL, web_search

class AgentTests(unittest.TestCase):
    def test_persistence_sessions_and_timestamp(self):
        with tempfile.TemporaryDirectory() as d:
            path=os.path.join(d,'memory.db')
            memory=Memory(path)
            memory.add('a','user','Explain quantum physics')
            memory.add('b','user','secret')
            memory.db.close()
            memory=Memory(path)
            history=memory.history('a')
            self.assertEqual(len(history),1)
            self.assertIn('+00:00',history[0][2])
            self.assertEqual(memory.matches('a','quantum',[])[0][0], 'Explain quantum physics')
            self.assertNotIn('secret',str(history))

    def test_one_tool_and_key_error(self):
        self.assertEqual(TOOL['function']['name'],'web_search')
        self.assertIn('error',web_search('hello',''))

    @patch('agent.urlopen')
    def test_search_filters_unsafe_urls(self,mock):
        class Response:
            def __enter__(self):
                return BytesIO(json.dumps({'web':{'results':[
                    {'title':'T','url':'https://example.org','description':'S'},
                    {'title':'Bad','url':'javascript:alert(1)'}]}}).encode())
            def __exit__(self,*args): return False
        mock.return_value=Response()
        result=web_search('test','dummy',count=99)
        self.assertEqual(len(result['results']),1)
        self.assertIn('count=8',mock.call_args.args[0].full_url)

if __name__=='__main__': unittest.main()
