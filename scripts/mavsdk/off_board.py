from mavsdk import System
import asyncio
import rospy
from offboard_mode.msg import drone
import threading

drone_ip = drone()

def drone_input_callback(msg: drone):
    # rospy.loginfo("received %s, providing to the drone",msg)
    global drone_ip
    # drone_ip = drone()
    drone_ip.roll = msg.roll
    drone_ip.pitch = msg.pitch
    drone_ip.thrust = msg.thrust
    drone_ip.yaw = msg.yaw
    drone_ip.servo = msg.servo


async def main():
    print("Started offboard mode, trying to use manual control")
    quad = System()
    # await quad.connect(system_address="udp://:14550")
    await quad.connect()
    # await drone.connect()
    # await drone.connect()

    print("--- Connecting")
    async for state in quad.core.connection_state():
        if(state.is_connected):
            print("--- Connected")
            break
    
    # Checking if Global Position Estimate is ok
    async for health in quad.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("--- Global position state is good enough for flying.")
            break
    
    # Arming the drone
    print("-- Arming")
    await quad.action.arm()

    # Takeoff the vehicle
    print("-- Taking off")
    await quad.action.takeoff()
    await asyncio.sleep(5)

    rospy.init_node("offboard_input",anonymous=True)
    # await quad.manual_control.set_manual_control_input(
    #         float(0), float(0), float(0.5), float(0)
    #         )
    # await quad.action.hold()
    # await asyncio.sleep(3)
    print("Trying to subscribe")
    rospy.Subscriber("/drone_input",drone,callback=drone_input_callback)
    print("Subscribed, trying to connect")
    # provide the joy input for mavsdk
    # await quad.manual_control.start_position_control()
    count = 0
    # while count<10:
    #     await quad.manual_control.set_manual_control_input(float(0),float(0),float(0.5),float(0))
    #     await asyncio.sleep(0.01)
    await print("Starting manual now")
    await quad.manual_control.start_position_control()
    while True:
        await print(drone_ip)
        await quad.manual_control.set_manual_control_input(float(drone_ip.roll), float(drone_ip.pitch), float(drone_ip.thrust), float(drone_ip.yaw))
        await asyncio.sleep(0.01)

    

asyncio.run(main())