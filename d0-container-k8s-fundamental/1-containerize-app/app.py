from flask import Flask, request, jsonify
import ipaddress

app = Flask(__name__)

@app.route('/cidr-to-subnet', methods=['GET'])
def cidr_to_subnet():
    cidr = request.args.get('cidr')
    try:
        # Create an IPv4Network object from the CIDR
        network = ipaddress.IPv4Network('0.0.0.0/' + cidr)
        # Return the subnet mask
        return jsonify({'subnet': str(network.netmask)})
    except ValueError:
        return jsonify({'error': 'Invalid CIDR'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
