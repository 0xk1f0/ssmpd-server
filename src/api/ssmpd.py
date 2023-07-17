import sys
import asyncio
import snapcast.control
from flask import Flask, jsonify, request
from mpd import MPDClient

# constants
SC_HOST = '127.0.0.1'
MPD_HOST = '127.0.0.1'

class ssmpdAPI:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.mpd = MPDClient()
        self.loop = asyncio.new_event_loop()
        self.app = self.__create_app__()

    def run(self):
        self.app.run(host=self.host, port=self.port, use_reloader=False, debug=False)

    def __create_snap_server__(self):
        try:
            loop = asyncio.new_event_loop()
            snapserver = loop.run_until_complete(
                snapcast.control.create_server(
                    loop, SC_HOST
                )
            )
            self.loop = loop
        except:
            sys.exit(1)
        return snapserver

    def __create_app__(self):
        app = Flask(__name__)

        @app.route('/api/version', methods=['GET'])
        def version():
            response = {'message': 'v0.0.1'}
            return jsonify(response)

        ### SNAPCAST ENDPOINTS ###

        @app.route('/api/scc/getClient', methods=['POST'])
        def scc_get_client():
            request_data = request.get_json()
            scc = self.__create_snap_server__()
            response = self.loop.run_until_complete(scc.client_status(
                request_data.get('client_id')
            ))
            return jsonify(response)

        @app.route('/api/scc/getClients', methods=['GET'])
        def scc_get_clients():
            scc = self.__create_snap_server__()
            rs_dict = {}
            for i in scc.clients:
                rs_dict[i.friendly_name] = i.identifier
            response = rs_dict
            return jsonify(response)

        @app.route('/api/scc/setClientVolume', methods=['POST'])
        def scc_set_client_volume():
            request_data = request.get_json()
            scc = self.__create_snap_server__()
            response = self.loop.run_until_complete(scc.client_volume(
                request_data.get('client_id'), request_data.get('volume')
            ))
            return jsonify(response)

        @app.route('/api/scc/setClientName', methods=['POST'])
        def scc_set_client_name():
            request_data = request.get_json()
            scc = self.__create_snap_server__()
            response = self.loop.run_until_complete(scc.client_name(
                request_data.get('client_id'), request_data.get('name')
            ))
            return jsonify(response)

        @app.route('/api/scc/getGroup', methods=['POST'])
        def scc_get_group():
            request_data = request.get_json()
            scc = self.__create_snap_server__()
            response = self.loop.run_until_complete(scc.group_status(
                request_data.get('group_id')
            ))
            return jsonify(response)

        @app.route('/api/scc/getGroups', methods=['GET'])
        def scc_get_groups():
            scc = self.__create_snap_server__()
            rs_dict = {}
            for i in scc.groups:
                rs_dict[i.friendly_name] = i.identifier
            response = rs_dict
            return jsonify(response)

        @app.route('/api/scc/setGroupName', methods=['POST'])
        def scc_set_group_name():
            request_data = request.get_json()
            scc = self.__create_snap_server__()
            response = self.loop.run_until_complete(scc.group_name(
                request_data.get('group_id'), request_data.get('name')
            ))
            return jsonify(response)

        @app.route('/api/scc/setGroupClients', methods=['POST'])
        def scc_set_group_clients():
            request_data = request.get_json()
            scc = self.__create_snap_server__()
            response = self.loop.run_until_complete(scc.group_clients(
                request_data.get('group_id'), request_data.get('clients')
            ))
            return jsonify(response)

        @app.route('/api/scc/getStreams', methods=['GET'])
        def scc_get_streams():
            scc = self.__create_snap_server__()
            rs_dict = {}
            for i in scc.streams:
                rs_dict[i.friendly_name] = i.identifier
            response = rs_dict
            return jsonify(response)

        @app.route('/api/scc/setStream', methods=['POST'])
        def scc_set_stream():
            request_data = request.get_json()
            scc = self.__create_snap_server__()
            response = self.loop.run_until_complete(scc.group_stream(
                request_data.get('group_id'), request_data.get('stream_id')
            ))
            return jsonify(response)

        ### MPD ENDPOINTS ###

        @app.route('/api/mpd/getInfo', methods=['POST'])
        async def mpd_getInfo():
            request_data = request.get_json()
            PORT = 6600 + (int(request_data.get('edp_num')) - 1)
            self.mpd.connect(MPD_HOST, PORT)
            response = self.mpd.status()
            self.mpd.disconnect()
            return jsonify(response)

        @app.route('/api/mpd/getStats', methods=['POST'])
        async def mpd_getStats():
            request_data = request.get_json()
            PORT = 6600 + (int(request_data.get('edp_num')) - 1)
            self.mpd.connect(MPD_HOST, PORT)
            response = self.mpd.stats()
            self.mpd.disconnect()
            return jsonify(response)

        @app.route('/api/mpd/setPlayback', methods=['POST'])
        async def mpd_getStats():
            request_data = request.get_json()
            PORT = 6600 + (int(request_data.get('edp_num')) - 1)
            ACTION = request_data.get('action')
            self.mpd.connect(MPD_HOST, PORT)
            match ACTION:
                case 'resume':
                    response = self.mpd.pause(0)

                case 'pause':
                    response = self.mpd.pause(1)
                
                case 'next':
                    response = self.mpd.next()
                
                case 'previous':
                    response = self.mpd.previous()

            self.mpd.disconnect()
            return jsonify(response)

        return app
