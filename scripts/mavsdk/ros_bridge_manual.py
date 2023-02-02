import rospy 
import asyncio
from offboard_mode.msg import drone
from mavsdk import System

def manual_callback(msg: drone):
    pitch = msg.pitch
    roll = msg.roll
    yaw = msg.yaw
    thrust = msg.thrust
    rospy.loginfo("Received info : %s",msg)

    # await drone.manual_control.set_manual_control_input(roll, pitch, thrust, yaw)

async def subscribe():
    rospy.Subscriber("/drone_input",drone,callback=manual_callback)


async def main():
    rospy.init_node("ros_bridge", anonymous=True)
    
    
    # connect to the drone
    drone = System()
    
    # await drone.connect(system_address="udp://:14540")
    await drone.connect()

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    # Checking if Global Position Estimate is ok
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break

    # set the manual control input after arming
    await drone.manual_control.set_manual_control_input(
        float(0), float(0), float(0.5), float(0)
    )

    # Arming the drone
    print("-- Arming")
    await drone.action.arm()

    # Takeoff the vehicle
    print("-- Taking off")
    await drone.action.takeoff()
    await asyncio.sleep(10)

    # set the manual control input after arming
    await drone.manual_control.set_manual_control_input(
        float(0), float(0), float(0.5), float(0)
    )

    print("-- Starting manual control")
    await drone.manual_control.start_position_control()

    # await subscribe()
    # rospy.spin()

if __name__ == "__main__":
    asyncio.run(main())