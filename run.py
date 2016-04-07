#!/usr/bin/env python
import tychedice

tychedice.app.config.from_object('config.TestConfiguration')


tychedice.app.run(host='127.0.0.1', port=8000, debug=True)
