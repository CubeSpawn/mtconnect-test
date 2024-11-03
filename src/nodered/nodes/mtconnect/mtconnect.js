module.exports = function(RED) {
    function MTConnectIn(config) {
        RED.nodes.createNode(this, config);
        const node = this;
        let interval;
        
        // Config
        node.url = config.url;
        node.interval = config.interval || 1000;
        node.dataItems = config.dataItems || [];
        
        // HTTP Client setup
        const axios = require('axios');
        const xml2js = require('xml2js');
        const parser = new xml2js.Parser();
        
        // Main polling function
        async function pollMTConnect() {
            try {
                // Get current state
                const response = await axios.get(`${node.url}/current`);
                
                // Parse XML response
                parser.parseString(response.data, (err, result) => {
                    if (err) {
                        node.error("Failed to parse MTConnect response");
                        return;
                    }
                    
                    // Extract data items
                    const streams = result.MTConnectStreams.Streams[0];
                    const deviceStreams = streams.DeviceStream[0];
                    
                    // Process data items
                    const data = {};
                    if (deviceStreams.DataItems) {
                        deviceStreams.DataItems[0].DataItem.forEach(item => {
                            data[item.$.name] = item.$.value;
                        });
                    }
                    
                    // Send data
                    node.send({
                        payload: data,
                        topic: "mtconnect/current"
                    });
                });
            } catch (error) {
                node.error("MTConnect polling error: " + error.message);
            }
        }
        
        // Start polling
        if (node.url) {
            interval = setInterval(pollMTConnect, node.interval);
        }
        
        // Cleanup on close
        node.on('close', function() {
            if (interval) {
                clearInterval(interval);
            }
        });
    }
    
    RED.nodes.registerType("mtconnect-in", MTConnectIn);
}