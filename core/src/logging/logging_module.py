import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='firewall.log',  # Log file name
    filemode='a'  # Append mode
)

def log_packet_decision(packet, score, action):
    """
    Log the decision made for a packet.
    """
    logging.info(f"Packet: {packet}, Score: {score}, Action: {action}")