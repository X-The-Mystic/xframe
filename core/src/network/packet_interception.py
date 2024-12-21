from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP
import pandas as pd
from datetime import datetime
import threading
import queue
import sqlite3
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='packet_capture.log'
)

class PacketSniffer:
    def __init__(self, interface="eth0", max_packets=1000):
        self.interface = interface
        self.packet_queue = queue.Queue(maxsize=max_packets)
        self.stop_sniffing = threading.Event()
        self.db_path = "packets.db"
        self.setup_database()
        
    def setup_database(self):
        """Initialize SQLite database for packet storage"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS packets
                    (timestamp TEXT,
                     src_ip TEXT,
                     dst_ip TEXT,
                     protocol TEXT,
                     length INTEGER,
                     src_port INTEGER,
                     dst_port INTEGER,
                     payload BLOB,
                     flags TEXT)''')
        conn.commit()
        conn.close()

    def packet_callback(self, packet):
        """Process each captured packet"""
        try:
            if IP in packet:
                packet_info = self.extract_packet_info(packet)
                self.packet_queue.put(packet_info)
                
        except Exception as e:
            logging.error(f"Error processing packet: {str(e)}")

    def extract_packet_info(self, packet):
        """Extract relevant information from packet"""
        info = {
            'timestamp': datetime.now().isoformat(),
            'src_ip': packet[IP].src,
            'dst_ip': packet[IP].dst,
            'protocol': packet[IP].proto,
            'length': len(packet),
            'src_port': None,
            'dst_port': None,
            'payload': bytes(packet.payload),
            'flags': None
        }

        if TCP in packet:
            info['protocol'] = 'TCP'
            info['src_port'] = packet[TCP].sport
            info['dst_port'] = packet[TCP].dport
            info['flags'] = str(packet[TCP].flags)
        elif UDP in packet:
            info['protocol'] = 'UDP'
            info['src_port'] = packet[UDP].sport
            info['dst_port'] = packet[UDP].dport

        return info

    def store_packets(self):
        """Store packets from queue to database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        while not self.stop_sniffing.is_set() or not self.packet_queue.empty():
            try:
                packet_info = self.packet_queue.get(timeout=1)
                c.execute('''INSERT INTO packets VALUES 
                           (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (packet_info['timestamp'],
                          packet_info['src_ip'],
                          packet_info['dst_ip'],
                          packet_info['protocol'],
                          packet_info['length'],
                          packet_info['src_port'],
                          packet_info['dst_port'],
                          packet_info['payload'],
                          packet_info['flags']))
                conn.commit()
                
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Error storing packet: {str(e)}")
                
        conn.close()

    def start(self):
        """Start packet capture"""
        # Start storage thread
        storage_thread = threading.Thread(target=self.store_packets)
        storage_thread.start()
        
        logging.info(f"Starting packet capture on interface {self.interface}")
        try:
            sniff(iface=self.interface,
                  prn=self.packet_callback,
                  store=0,
                  stop_filter=lambda _: self.stop_sniffing.is_set())
        except Exception as e:
            logging.error(f"Error in packet capture: {str(e)}")
        
        # Wait for storage thread to complete
        storage_thread.join()

    def stop(self):
        """Stop packet capture"""
        self.stop_sniffing.set()
        logging.info("Stopping packet capture")

def main():
    # Create and start sniffer
    sniffer = PacketSniffer(interface="eth0")  # Change interface as needed
    
    try:
        sniffer.start()
    except KeyboardInterrupt:
        sniffer.stop()
        print("\nPacket capture stopped")

if __name__ == "__main__":
    main()
