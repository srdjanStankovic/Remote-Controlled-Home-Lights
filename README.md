# Remote Controlled Home Lights
                            %%%                            
                #%,         %%(         %%#                
                 %%(        %%*        %%%                 
                  ,%%       (%        %%                   
                    #     #%%%%%*     ,                    
                      #%#........,%%,                      
         %%%%%%%%,  %%..............%%   #%%%%%%%%         
                   /%................,%                    
                   %%....&@*@@@/@#....%.                   
                   ,%...|..........@..%                    
                    *%..#.........(.(%                     
                      (%.,......,.,%                       
                       %,#......%.%.                       
                       %#./.....,.%                        
                       /%.%....,..%                        
                        %%%%%%%%%%#                        
                           %%%%                           
                           .,,,                            
                                                                                        

In this project, I connected two Sonoff switches over Raspberry Pi3 to WolkAbout IoT Platform to control light at my home. One Sonoff switch is installed to my lamp in the dining room and another one to background light on the kitchen working area.

# Prerequisite

Hardware:
 * [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
 * [Sonoff Switches](https://www.sonoff.in/index.php?route=product/product&path=62&product_id=75)

Software:
 * Python3 with installed pip. **NOTE:** scripts and dependencies don't support Python2!
 * [Sonoff-Switch-Control](https://github.com/srdjanStankovic/Sonoff-Switch-Control) python script
 * [WolkAbout IoT Platform account](https://demo.wolkabout.com/#/get-started)
 * [wolk-connect](https://pypi.org/project/wolk-connect/) library

# Usage

#### 1'st step
Create account on [WolkAbout](https://demo.wolkabout.com/#/get-started). Upload template `Sonoff-Switches.json` from this repo and [create device]((https://www.youtube.com/watch?v=QllMw9Tw2ns)). As output of this action you will get device key & password. Save this, it will be used in step 4.

#### 2'nd step
Clone this repo to RPI with following command:

`git clone --recurse-submodules https://github.com/srdjanStankovic/Remote-Controlled-Home-Lights.git`

#### 3'rd step
Navigate to path `Remote-Controlled-Home-Lights/Sonoff-Switch-Control/`. Then you need to connect, configure and test your both Sonoff switches to your WiFi network following this repo [Sonoff-Switch-Control](https://github.com/srdjanStankovic/Sonoff-Switch-Control) guide. You actually downloaded this repo as submodule and you are navigated on it's location on your RPI.

#### 4'th step
When you succefully control your Sonoff's navigate one folder back to `Remote-Controlled-Home-Lights/`. Here insert **key** and **password** into `the_home_gateway.py` file(key and password are given while device is created on WolkAbout- described in 1'st step):
```
def main():
    device = wolk.Device(
        key="some-key",
        password="some-password",
        actuator_references=[SWITCH1_REF, SWITCH2_REF],
    )
```

#### 5'th step
Run `python3 the_home_gateway.py` in console and switches will become connected on WolkAbout.
Add Actuator widgets and I become enabled to control it. It looks similar to this:

<img width="272" alt="capture" src="https://user-images.githubusercontent.com/8199494/51498816-403e4c00-1dc8-11e9-9b69-c41bc9acaf73.PNG">

#### 6'th step (Optional)
At the end I deployed `the_home_gateway.py` file as systemctl service following ***Method 4: SYSTEMD*** from [THIS](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/) guide. This is good beacuse service will continue to run in background and even when any kind of reset ocuurs.


# Conclusion
Now, I'm able to control my lamp and kitchen light over my phone. Web I used rarely, sometimes when I read on my laptop.
Idea is to continue with this project and integrate voice control platform with my RPI or with WolkAbout.
