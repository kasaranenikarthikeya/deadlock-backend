from flask import Flask, request, jsonify
from flask_cors import CORS
from graph import ResourceAllocationGraph
import logging

app = Flask(__name__)

# Enhanced CORS configuration with proper headers
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://deadlock-p4ty.onrender.com"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

graph = ResourceAllocationGraph()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/process', methods=['POST'])
def add_process():
    try:
        data = request.json
        process = data.get('process')
        if not process:
            return jsonify({'success': False, 'error': 'Process ID is required'}), 400
        success = graph.add_process(process)
        logger.info(f"Add process {process}: {'Success' if success else 'Failed'}")
        return jsonify({'success': success, 'graph': graph.get_graph_state()})
    except Exception as e:
        logger.error(f"Error adding process: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/resource', methods=['POST'])
def add_resource():
    try:
        data = request.json
        resource = data.get('resource')
        if not resource:
            return jsonify({'success': False, 'error': 'Resource ID is required'}), 400
        success = graph.add_resource(resource)
        logger.info(f"Add resource {resource}: {'Success' if success else 'Failed'}")
        return jsonify({'success': success, 'graph': graph.get_graph_state()})
    except Exception as e:
        logger.error(f"Error adding resource: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/request', methods=['POST'])
def request_resource():
    try:
        data = request.json
        process, resource = data.get('process'), data.get('resource')
        if not process or not resource:
            return jsonify({'success': False, 'error': 'Process and Resource IDs are required'}), 400
        success = graph.request_resource(process, resource)
        logger.info(f"Request resource {resource} by {process}: {'Success' if success else 'Failed'}")
        return jsonify({'success': success, 'graph': graph.get_graph_state()})
    except Exception as e:
        logger.error(f"Error requesting resource: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/allocate', methods=['POST'])
def allocate_resource():
    try:
        data = request.json
        process, resource = data.get('process'), data.get('resource')
        if not process or not resource:
            return jsonify({'success': False, 'error': 'Process and Resource IDs are required'}), 400
        success = graph.allocate_resource(process, resource)
        logger.info(f"Allocate resource {resource} to {process}: {'Success' if success else 'Failed'}")
        return jsonify({'success': success, 'graph': graph.get_graph_state()})
    except Exception as e:
        logger.error(f"Error allocating resource: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/node/<id>', methods=['DELETE'])
def remove_node(id):
    try:
        success = graph.remove_node(id)
        logger.info(f"Remove node {id}: {'Success' if success else 'Failed'}")
        return jsonify({'success': success, 'graph': graph.get_graph_state()})
    except Exception as e:
        logger.error(f"Error removing node: {str(e)}")


        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/edge', methods=['DELETE'])
def remove_edge():
    try:
        data = request.json
        process, resource = data.get('process'), data.get('resource')
        if not process or not resource:
            return jsonify({'success': False, 'error': 'Process and Resource IDs are required'}), 400
        success = graph.remove_edge(process, resource)
        logger.info(f"Remove edge {process}-{resource}: {'Success' if success else 'Failed'}")
        return jsonify({'success': success, 'graph': graph.get_graph_state()})
    except Exception as e:
        logger.error(f"Error removing edge: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset_graph():
    try:
        graph.reset_graph()
        logger.info("Graph reset successfully")
        return jsonify({
            'success': True,
            'graph': graph.get_graph_state(),
            'message': 'Graph has been fully reset'
        })
    except Exception as e:
        logger.error(f"Error resetting graph: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/deadlock', methods=['GET'])
def check_deadlock():
    try:
        cycle = graph.check_deadlock()
        logger.info(f"Deadlock check: {'Cycle found' if cycle else 'No cycle'}")
        return jsonify({'cycle': cycle, 'graph': graph.get_graph_state()})
    except Exception as e:
        logger.error(f"Error checking deadlock: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/undo', methods=['POST'])
def undo():
    try:
        graph.undo()
        logger.info("Undo action")
        return jsonify({'success': True, 'graph': graph.get_graph_state()})
    except Exception as e:
        logger.error(f"Error undoing action: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/redo', methods=['POST'])
def redo():
    try:
        graph.redo()
        logger.info("Redo action")
        return jsonify({'success': True, 'graph': graph.get_graph_state()})
    except Exception as e:
        logger.error(f"Error redoing action: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/graph', methods=['GET'])
def get_graph():
    try:
        logger.info("Fetched graph state")
        return jsonify({'graph': graph.get_graph_state()})
    except Exception as e:
        logger.error(f"Error fetching graph state: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
