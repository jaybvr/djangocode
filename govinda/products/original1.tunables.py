

setenv=False
exits=False

for i in sys.argv:
    if not i in 'tunables.py':
        if i=='--help':
            print('======================================================================================================================================')
            print('tunables.py is the utility to verify and update the current configuration options of PowerVC environement to have better performance')
            print('use "python tunables.py" to check the current configuration if it is having the recommended values')
            print('use "python tunables.py -s" for setting the recommended tunables')
            print('======================================================================================================================================')
            exits=True
        elif i=='-s':
            setenv=True
            print (i)
        else :
            print('======================================================================================================================================')
            print('Invalid usage')
            print('use "python tunables.py --help" to know the right usage')
            print('======================================================================================================================================')
            exits=True


if not exits:

    config=configparser.ConfigParser()

    print('======================================================================================================================================')
    print('+++++++++++++++++++++++++++++++++   Neutron settings    ++++++++++++++++++++++++++++++++++++')
    print('======================================================================================================================================')

    if os.path.exists('/etc/neutron/neutron.conf'):
            config.read('/etc/neutron/neutron.conf')
            
            if config.has_option('DEFAULT','agent_down_time'):
                if (config.get('DEFAULT','agent_down_time')!='360'):
                    print('Recommended value for "/etc/neutron/neutron.conf.DEFAULT.agent_down_time" is  360, however it has '+config.get('DEFAULT','agent_down_time'))
                    if setenv:
                        config.set('DEFAULT','agent_down_time','360')
                        print('value for "/etc/neutron/neutron.conf.DEFAULT.agent_down_time" has been set to 360')
                else:
                    print('"/etc/neutron/neutron.conf.DEFAULT.agent_down_time" has the recommended value 360')
            else:
                print('Option agent_down_time does not exist')


            if config.has_option('DEFAULT','rpc_response_timeout'):
                if (config.get('DEFAULT','rpc_response_timeout')!='18000/1800 (NL)'):
                    print('Recommended value for "/etc/neutron/neutron.conf.DEFAULT.rpc_response_timeout" is  18000/1800 (NL), however it has '+config.get('DEFAULT','rpc_response_timeout'))
                    if setenv:
                        config.set('DEFAULT','rpc_response_timeout','18000/1800 (NL)')
                        print('value for /etc/neutron/neutron.conf.DEFAULT.rpc_response_timeout" has been set to 18000/1800 (NL)')
                else:
                    print('"/etc/neutron/neutron.conf.DEFAULT.rpc_response_timeout" has the recommended value 18000/1800 (NL)')
            else:
                print('Option rpc_response_timeout does not exist')


            if config.has_option('DEFAULT','rpc_workers'):
                if (config.get('DEFAULT','rpc_workers')!='52'):
                    print('Recommended value for "/etc/neutron/neutron.conf.DEFAULT.rpc_workers" is  52, however it has '+config.get('DEFAULT','rpc_workers'))
                    if setenv:
                        config.set('DEFAULT','rpc_workers','52')
                        print('value for "/etc/neutron/neutron.conf.DEFAULT.rpc_workers" has been set to recommended value 52')
                else:
                    print('"/etc/neutron/neutron.conf.DEFAULT.rpc_workers" has the recommended value 52')
            else:
                print('Option rpc_workers does not exist')


            if config.has_option('DEFAULT','rpc_conn_pool_size'):
                if (config.get('DEFAULT','rpc_conn_pool_size')!='300'):
                    print('Recommended value for "/etc/neutron/neutron.conf.DEFAULT.rpc_conn_pool_size" is  300, however it has '+config.get('DEFAULT','rpc_conn_pool_size'))
                    if setenv:
                        config.set('DEFAULT','rpc_conn_pool_size','300')
                        print('value for "/etc/neutron/neutron.conf.DEFAULT.rpc_conn_pool_size" has been set to the recommended value 300')
                else:
                    print('"/etc/neutron/neutron.conf.DEFAULT.rpc_conn_pool_size" has the recommended value 300')
            else:
                print('Option rpc_conn_pool_size does not exist')


            if config.has_option('DEFAULT','rpc_state_report_workers'):
                if (config.get('DEFAULT','rpc_state_report_workers')!='10'):
                    print('Recommended value for "/etc/neutron/neutron.conf.DEFAULT.rpc_state_report_workers" is  10, however it has '+config.get('DEFAULT','rpc_state_report_workers'))
                    if setenv:
                        config.set('DEFAULT','rpc_state_report_workers','10')
                        print('value for "/etc/neutron/neutron.conf.DEFAULT.rpc_state_report_workers" has been set to the recommended value 10')
                else:
                    print('"/etc/neutron/neutron.conf.DEFAULT.rpc_state_report_workers" has the recommended value 10')
            else:
                print('Option rpc_state_report_workers does not exist')


            if config.has_option('DEFAULT','executor_thread_pool_size'):
                if (config.get('DEFAULT','executor_thread_pool_size')!='2048'):
                    print('Recommended value for "/etc/neutron/neutron.conf.DEFAULT.executor_thread_pool_size" is  2048, however it has '+config.get('DEFAULT','executor_thread_pool_size'))
                    if setenv:
                        config.set('DEFAULT','executor_thread_pool_size','2048')
                        print('value for "/etc/neutron/neutron.conf.DEFAULT.executor_thread_pool_size" has been set to the recommended value 2048')
                else:
                    print('"/etc/neutron/neutron.conf.DEFAULT.executor_thread_pool_size" has the recommended value 2048')
            else:
                print('Option executor_thread_pool_size does not exist')


            if config.has_option('DEFAULT','report_interval'):
                if (config.get('DEFAULT','report_interval')!='150'):
                    print('Recommended value for "/etc/neutron/neutron.conf.DEFAULT.report_interval" is  150, however it has '+config.get('DEFAULT','report_interval'))
                    if setenv:
                        config.set('DEFAULT','report_interval','150')
                        print('value for "/etc/neutron/neutron.conf.DEFAULT.report_interval" has been set to the recommended value 150')
                else:
                    print('"/etc/neutron/neutron.conf.DEFAULT.report_interval" has the recommended value 150')
            else:
                print('Option report_interval does not exist')

            with open('/etc/neutron/neutron.conf','w') as configfile:
                    config.write(configfile)


    else:
        print('Neutron file does not exists /etc/neutron/neutron.conf') 

    print('======================================================================================================================================')

    print('======================================================================================================================================')
    print('+++++++++++++++++++++++++++++++++  Nova settings    ++++++++++++++++++++++++++++++++++++')
    print('======================================================================================================================================')
    if os.path.exists('/etc/nova/nova.conf'):
        print('File /etc/nova/nova.conf exists')
    else:
        print('Nova file does not exists /etc/nova/nova.conf')     


    print('======================================================================================================================================')
    print('======================================================================================================================================')

    print('======================================================================================================================================')
    print('+++++++++++++++++++++++++++++++++  Cinder settings    ++++++++++++++++++++++++++++++++++++')
    print('======================================================================================================================================')

    if os.path.exists('/etc/cinder/cinder.conf'):
        print('File /etc/cinder/cinder.conf exists')
    else:
        print('Cinder file does not exists /etc/cinder/cinder.conf')     


    print('======================================================================================================================================')
    print('======================================================================================================================================')

    print('======================================================================================================================================')
    print('+++++++++++++++++++++++++++++++++  Keystone settings    ++++++++++++++++++++++++++++++++++++')
    print('======================================================================================================================================')
    if os.path.exists('/etc/keystone/keystone.conf'):
        print('File /etc/keystone/keystone.conf exists')
    else:
        print('Keystone file does not exists /etc/keystone/keystone.conf')   



    print('======================================================================================================================================')
    print('======================================================================================================================================')

    print('======================================================================================================================================')
    print('+++++++++++++++++++++++++++++++++  Other configuration settings    ++++++++++++++++++++++++++++++++++++')
    print('======================================================================================================================================')




    print('======================================================================================================================================')
