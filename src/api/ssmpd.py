import sys
import asyncio
import snapcast.control
from flask import Flask, jsonify, render_template

class ssmpdAPI:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.loop = asyncio.get_event_loop()
        self.app = self.__create_app__()

    def run(self):
        self.app.run(host='127.0.0.1', port='5000', use_reloader=False, debug=False)

    def __create_snap_server__(self):
        try:
            snapserver = self.loop.run_until_complete(snapcast.control.create_server(
                    self.loop, self.host
                )
            )
        except:
            sys.exit(1)
        return snapserver

    def __create_app__(self):
        # create flask endpoint
        app = Flask(__name__)

        # flask routes
        @app.route('/api/version', methods=['GET'])
        def version():
            response = {'message': 'v0.0.1'}
            return jsonify(response)

        @app.route('/api/getClients', methods=['GET'])
        def getClients():
            scc = self.__create_snap_server__()
            rs_dict = {}
            for i in scc.clients:
                rs_dict[i.friendly_name] = i.identifier
            response = rs_dict
            return jsonify(response)

        @app.route('/api/getGroups', methods=['GET'])
        def getGroups():
            scc = self.__create_snap_server__()
            rs_dict = {}
            for i in scc.groups:
                rs_dict[i.friendly_name] = i.identifier
            response = rs_dict
            return jsonify(response)

        @app.route('/api/getStreams', methods=['GET'])
        def getStreams():
            scc = self.__create_snap_server__()
            rs_dict = {}
            for i in scc.streams:
                rs_dict[i.friendly_name] = i.identifier
            response = rs_dict
            return jsonify(response)

        return app
