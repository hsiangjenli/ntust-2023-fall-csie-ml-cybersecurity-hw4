from scapy.all import *
import numpy as np
from PIL import Image
import argparse
import os

# parse arguments
parser = argparse.ArgumentParser(description='Convert pcap to images')

parser.add_argument('--pcap', type=str, help='pcap file to convert', required=True)
parser.add_argument('--output', type=str, help='output directory', default='output')
parser.add_argument('--width', type=int, help='width of image', default=28)
parser.add_argument('--height', type=int, help='height of image', default=28)

args = parser.parse_args()

protocal_map = {
    6: "TCP",
    17: "UDP"
}

os.makedirs(args.output, exist_ok=True)

def packets_to_flows(packets):

    flows = {}

    for packet in packets:
        try:
            protocol = protocal_map[packet['IP'].proto]
            # only keep TCP and UDP packets
            if protocol in ["TCP", "UDP"]:
                dst_ip = packet['IP'].dst
                dst_port = packet[protocol].dport
                src_ip = packet['IP'].src
                src_port = packet[protocol].sport
            
            key = f"{protocol}_{src_ip}_{src_port}_{dst_ip}_{dst_port}"

            if key not in flows and packet[protocol]:
                flows[key] = []
                flows[key].append(bytes(packet[protocol])[8:])

            elif packet[protocol]:
                flows[key].append(bytes(packet[protocol])[8:])

        except:
            pass
    
    return flows

if __name__ == "__main__":

    packets = rdpcap(args.pcap)
    flows = packets_to_flows(packets)
    
    w, h = args.width, args.height
    
    for key in flows:
        arrs = []

        # avoid duplicate in flows
        for data in set(flows[key]):
            arr = np.frombuffer(data, dtype=np.uint8)
            arrs.append(arr)

        arr = np.concatenate(arrs)
        
        # check if array is too short, then pad with zeros
        if len(arr) < w*h:
            arr = np.concatenate((arr, np.zeros(w*h-len(arr), dtype=np.uint8)))
        else:
            arr = arr[:w*h]
        
        arr = arr.reshape((w, h))
        img = Image.fromarray(arr, 'L')

        file_name = args.pcap.split(".")[0]
        file_name = file_name.split("/")[-1]

        # save image
        img.save(os.path.join(args.output,  file_name + "_" + str(key)+'.png'))