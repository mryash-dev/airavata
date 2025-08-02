#!/usr/bin/env python3
"""
Simple test script to verify Apache Airavata services are running
"""

import socket
import time

def test_port(host, port, service_name):
    """Test if a port is listening"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ {service_name} (port {port}) - LISTENING")
            return True
        else:
            print(f"❌ {service_name} (port {port}) - NOT LISTENING")
            return False
    except Exception as e:
        print(f"❌ {service_name} (port {port}) - ERROR: {e}")
        return False

def main():
    print("🧪 Testing Apache Airavata Services")
    print("=" * 40)
    
    services = [
        ("localhost", 8930, "Airavata API Server"),
        ("localhost", 18800, "Agent Service"),
        ("localhost", 18889, "Research Service"),
        ("localhost", 8050, "File Service"),
        ("localhost", 15672, "RabbitMQ Management"),
        ("localhost", 3306, "MariaDB"),
        ("localhost", 9092, "Kafka"),
        ("localhost", 2181, "ZooKeeper"),
    ]
    
    working_services = 0
    total_services = len(services)
    
    for host, port, name in services:
        if test_port(host, port, name):
            working_services += 1
        time.sleep(0.5)
    
    print("\n" + "=" * 40)
    print(f"📊 Results: {working_services}/{total_services} services working")
    
    if working_services == total_services:
        print("🎉 All services are running correctly!")
        print("\n✅ Apache Airavata is ready to use!")
        print("\nNext steps:")
        print("1. Use Thrift clients to connect to the services")
        print("2. Install the Python SDK: pip install airavata-python-sdk")
        print("3. Use the Java client examples in examples/airavata-api-java-client-samples/")
        print("4. Access RabbitMQ Management at http://localhost:15672")
        print("   (username: airavata, password: airavata)")
    else:
        print("⚠️  Some services are not responding")
        print("\nTroubleshooting:")
        print("1. Check container logs: docker logs airavata-monolithic")
        print("2. Restart services: docker-compose restart")
        print("3. Check if all containers are running: docker ps")

if __name__ == "__main__":
    main() 