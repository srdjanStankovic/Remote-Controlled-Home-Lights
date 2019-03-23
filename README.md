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
Firstly I connect, configure and test my both Sonoff switches to my WiFi network following [Sonoff-Switch-Control](https://github.com/srdjanStankovic/Sonoff-Switch-Control) guide.

#### 2'nd step
As second I create account on WolkAbout, upload template `Sonoff-Switches.json` and [create device]((https://www.youtube.com/watch?v=QllMw9Tw2ns)). As output of this action I get device key & password.

#### 3'rd step
Then I `ssh` to my RPI and install WolkAbout lib as `pip install wolk-connect`. My RPI is connected on the same WiFi as mine Sonoff switches. 
Clone this repo to RPI with following command:

`git clone --recurse-submodules https://github.com/srdjanStankovic/Remote-Controlled-Home-Lights.git`

Then insert key and password in `sonoff-switches.py` file:
```
def main():
    device = wolk.Device(
        key="some-key",
        password="some-password",
        actuator_references=[SWITCH1_REF, SWITCH2_REF],
    )
```

#### 4'th step
Run `sonoff-switches.py` in console and switches become connected on WolkAbout.
Add Actuator widgets and I become enabled to control it. It looks similar to this:

<img width="272" alt="capture" src="https://user-images.githubusercontent.com/8199494/51498816-403e4c00-1dc8-11e9-9b69-c41bc9acaf73.PNG">

#### 5'th step
At the end I deployed `sonoff-switches.py` file as systemctl service following ***Method 4: SYSTEMD*** from [THIS](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/) guide.

# Conclusion
Now, I'm able to control my lamp and kitchen light over my phone . Web I used rarely, sometimes when I read on my laptop. Idea is to continue with this project and integrate voice control platform with my RPI or with WolkAbout.
