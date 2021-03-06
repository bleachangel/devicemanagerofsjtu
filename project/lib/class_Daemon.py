'''this class defines class: Daemon'''

import dbus
import dbus.glib
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import sys
import gtk
import pynotify
from class_Device import Device


class Daemon(object):
    '''daemon of device manager listening to HAL signal'''
    def __init__(cls, manager):
        '''init of daemon'''
        cls.__manager=manager

        DBusGMainLoop(set_as_default=True)
        cls.__bus=dbus.SystemBus()
        obj=cls.__bus.get_object('org.freedesktop.Hal','/org/freedesktop/Hal/Manager')
        cls.__hal_manager=dbus.Interface(obj, 'org.freedesktop.Hal.Manager')

        # handle will be invoked when global device list is changed
        cls.__hal_manager.connect_to_signal('DeviceAdded', lambda *args: cls.handle('DeviceAdded',*args))
        cls.__hal_manager.connect_to_signal('DeviceRemoved', lambda *args: cls.handle('DeviceRemoved', *args))
        cls.__hal_manager.connect_to_signal('NewCapability', lambda *args: cls.handle('NewCapability', *args))

        # add listenerso for all devices
        deviceNames=cls.__hal_manager.GetAllDevices()

        # add icon at notification area
        cls.__icon=gtk.StatusIcon()
        cls.__icon.set_from_stock(gtk.STOCK_ABOUT)

        # redirect error message
        #error=sys.stderr
        #errfile=file('../log/err','w+')
        #sys.stderr=errfile # eception to do

        for name in deviceNames:
            cls.addDevSigRecv(name)
            device_dbus_obj=cls.__bus.get_object("org.freedesktop.Hal",name)
            properties=device_dbus_obj.GetAllProperties(dbus_interface="org.freedesktop.Hal.Device")
            cls.__manager.appendDeviceList(Device(name, properties))

        #sys.stderr=error
        #errfile.close()

    def addDevSigRecv(cls, udi):
        cls.__bus.add_signal_receiver(lambda *args: cls.propertyModified(udi, *args),"PropertyModified","org.freedesktop.Hal.Device","org.freedesktop.Hal",udi)

    def propertyModified(cls, udi, num_changed, change_list):
        '''this method is called when signals on the Device interface is received'''
        print 'in modified'
        print udi,num_changed,change_list

        n=num_changed #alias
        list=change_list #alias

        #print "PropertiesModified, device = %s"%udi
        for i in list:
            name=i[0] #property name
            removed=i[1]
            added=i[2]

            #print " key=%s, rem=%d, add=%d"%(name, removed, added)
            if name=='info.parent':
                pass# to do
            else:
                udi_obj=cls.__bus.get_object("org.freedesktop.Hal", udi)
                device=cls.__manager.getDeviceObj(udi)
                if udi_obj.PropertyExists(name, dbus_interface="org.freedesktop.Hal.Device"):
                    device.setProperty(name,udi_obj.GetProperty(name, dbus_interface="org.freedesktop.Hal.Device"))
                else:
                    device.remProperty(name)

    def loop(cls):
        cls.__loop=gobject.MainLoop()
        cls.__loop.run()

    def notify(cls, title, info):
        pynotify.init("dev")
        n=pynotify.Notification(title, info)
        n.attach_to_status_icon(cls.__icon)
        n.show()

    def handle(cls, signal, udi, *args):
        '''handle of the signals'''
        product=str(cls.__manager.getDeviceProduct(udi))
        if signal=='DeviceAdded':
            cls.notify("Add", product)
            print 'add',udi
            cls.__manager.update()
        elif signal=='DeviceRemoved':
            cls.notify("Remove", product)
            print 'remove',udi
            cls.__manager.update()
        elif signal=='NewCapability':
            cls.notify("Modify", product)
            print 'new',udi
            cls.__manager.update()
