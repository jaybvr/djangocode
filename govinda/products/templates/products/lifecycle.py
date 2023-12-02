#powervc_tempest.tests.Regression.FVT.extended_bvt.fvt_test_lifecycle
#/var/lib/jenkins/workspace/RTC_code_copy/powervc-tempest/powervc_tempest/tests/Regression/FVT/extended_bvt/fvt_test_lifecycle.py
#test_001_attach_detach_active_vm	5 min 42 sec	Passed
"""test_003_resize_server_active	7 min 11 sec	Passed
test_004_attach_detach_inactive_vm	7 min 24 sec	Passed
test_005_capture_image_on_inactive_vm	11 min	Passed
test_006_stop_start_server	11 min	Passed
test_007_resize_server_inactive	17 min	Passed
test_008_hard_restart_server	6 min 0 sec	Passed
test_009_clone_vm_active_ok_default_group	7 min 51 sec	Passed
test_010_list_servers_with_detail	30 sec	Passed
test_011_compute_host_unonboard_onboard_VM	1 min 26 sec	Passed
test_012_clone_vm_inactive_ok_default_group	19 min	Passed
test_013_get_server_by_id	1 min 0 sec	Passed
test_014_instance_snapshot	1 min 57 sec	Passed
test_015_vm_snapshot	1 min 17 sec	Passed
test_016_cleanup_all_resources	1 ms	Passed
test_017_register_cpn_n_detail	11 min	Passed
"""


import time
import random
from tempest.common import waiters
from powervc_tempest.tests import base_test
from tempest.lib.common.utils import data_utils
from nose.plugins.attrib import attr
from powervc_tempest import powervc_config
from tempest.lib import exceptions
import uuid
# from powervc_tempest import meta
import threading
from powervc_tempest.common.powervc_ssh import PowerVCClient as sshclient
CONF = powervc_config.CONF

# NUM_OF_VMS = 1
vm_name_onboarded = ""



@attr('fvtr')
class FVTLifecycle(base_test.BaseTestCase):

    __test__ = True

    @classmethod
    def setup_clients(cls):
        # The below line has to be removed in the previous versions
        super(FVTLifecycle, cls).setup_clients()
        #cls.server_name = data_utils.rand_name(cls.__name__)
        cls.server_image = cls.os.config.image.image_name
        cls.servers_client = cls.os.servers_client
        cls.image_client_v2 = cls.os.image_client_v2
        cls.images_client = cls.os.images_client
        cls.flavors_client = cls.os.flavors_client
        cls.flavour_ram = cls.os.config.compute.flavour_ram
        cls.flavour_vcpus = cls.os.config.compute.flavour_vcpus
        cls.flavour_disk = cls.os.config.compute.flavour_disk
        cls.flavour_max_proc_units = cls.os.config.compute.flavour_max_proc_units
        cls.flavour_procunits = cls.os.config.compute.flavour_procunits
        cls.flavour_min_proc_units = cls.os.config.compute.flavour_min_proc_units
        cls.flavour_name =  cls.os.config.compute.flavour_name
        cls.cleanup_all_resources = cls.os.config.compute.cleanup_all_resources
        cls.network_client = cls.os.network_client
        cls.compute_client = cls.os.compute_client
        cls.NUM_OF_VMS= cls.os.config.compute.no_of_vm_for_extended_bvt
        cls.volume_client = cls.os.volume_client
        cls.volumes_v3_client = cls.os.volumes_v3_client
        cls.volume_types_v3_client=cls.os.volume_types_v3_client
        cls.network_name = cls.os.config.network.network_name
        cls.hosts_client = cls.os.hosts_client
        cls.powervc_ip = cls.os.config.identity.powervc_ip
        cls.vm_fixed_ip = cls.os.config.network.network_fixed_ip1
        cls.network_name = cls.os.config.network.network_name
        cls.server_name = data_utils.rand_name(cls.__name__)
        cls.volume_client = cls.os.volume_client
        cls.vm_snapshots_client = cls.os.vm_snapshots_client
        cls.config_file_volume_name = cls.os.config.volume.volume_name
        cls.servers_client = cls.os.servers_client
        cls.flavour_id = None
        cls.cpn_client = cls.os.cpn_client
        cls.compute_plane_node_list = \
            CONF.identity.compute_plane_node_list
        if CONF.powervc.compute == "powervm":
            cls.HMC_user_id = cls.os.config.compute.HMC_user_id
            cls.HMC_password = cls.os.config.compute.HMC_password
            cls.HMC_access_ip = cls.os.config.compute.HMC_access_ip
            cls.hmc_obj = sshclient(host=cls.HMC_access_ip,
                                    username=cls.HMC_user_id,
                                    password=cls.HMC_password,
                                    channel_timeout=600)


    @classmethod
    def resource_setup(cls):
        super(FVTLifecycle, cls).resource_setup(compute=True,
                                                storage=True,
                                                network=True,
                                               image=True)
        if cls.cleanup_all_resources.lower() == 'false':
            cls.list_of_server_ids = cls._get_server_ids()
            cls.flavour_id = cls._create_flavour()
            if len(cls.list_of_server_ids) != int(cls.NUM_OF_VMS):
                time.sleep(300)
                vm_threads = []
                ips_to_be_used_for_deploy = cls._get_ips_to_be_used_for_deploys()
                for index, fixed_ip in enumerate(ips_to_be_used_for_deploy):
                    vm_thread = threading.Thread(
                        target=cls._deploy_vms, args=(index, fixed_ip, cls.flavour_id, ))
                    vm_threads.append(vm_thread)
                    vm_thread.start()

                for vm_thread in vm_threads:
                    try:
                        vm_thread.join()
                    except Exception as e:
                        print(('Something went wrong while waiting for the thread to '
                            'complete: %s' % str(e)))
                        # cls.resource_cleanup()
                        raise

            if len(cls.list_of_server_ids) < int(cls.NUM_OF_VMS):
                raise Exception(f"Total number of VMs deployed: {str(len(cls.list_of_server_ids))}."
                                f" Expected number of VMs: {str(cls.NUM_OF_VMS)}")

    @classmethod
    def _get_ips_to_be_used_for_deploys(cls):
        fixed_ips_set = set()
        for index in range(int(cls.NUM_OF_VMS)):
            fixed_ip='network_fixed_ip' + str(index + 1)
            fixed_ip_value = getattr(cls.os.config.network, fixed_ip)
            fixed_ips_set.add(fixed_ip_value)
        print(f"_get_ips_to_be_used_for_deploys, "
              f"fixed_ips_set from config: {fixed_ips_set}")
        if len(fixed_ips_set) == 0:
            raise Exception("IPs are missing in config file.")
        if len(cls.list_of_server_ids) > 0:
            for server_id in cls.list_of_server_ids:
                server_ip = cls._get_server_ip(server_id)
                if server_ip:
                    print(f"_get_ips_to_be_used_for_deploys,"
                          f" server_id: {server_id}, server_ip: {server_ip}")
                    if server_ip in fixed_ips_set:
                        fixed_ips_set.remove(server_ip)
        print(f"_get_ips_to_be_used_for_deploys, final"
              f" list(fixed_ips_set): {list(fixed_ips_set)}")
        return list(fixed_ips_set)
    
    @classmethod
    def _get_server_ids(cls):
        list_of_server_ids = []
        body = cls.servers_client.list_servers()
        print(f"Value of list servers is : {body}")
        for server_details in body['servers']:
            for key , value in server_details.items():
                if key == 'id':
                    print(f"Value of server_id existing is {key}: {value}")
                    list_of_server_ids.append(value)
        print(f"List of server ID existing is : {list_of_server_ids} ")
        return list_of_server_ids
    
    @classmethod
    def _create_flavour(cls):
        name = "extendedbvt-flavour"
        ram =  cls.flavour_ram
        vcpus = cls.flavour_vcpus
        disk = cls.flavour_disk
        swap = 0
        # Check if flavour already exists
        flavour_id = None
        params = {'is_public' : None}
        resp, body_list_flavours = cls.flavors_client.list_flavors(
            detail=True, **params)
        print(f"resp: {resp}, body_list_flavours: {body_list_flavours}")
        for flavor_detail in body_list_flavours['flavors']:
            if flavor_detail.get('name') == name:
                flavour_id = flavor_detail.get('id')
                print(f" Flavor id already exists: {flavour_id}")
                break
        if flavour_id is None:
            resp, body = cls.flavors_client.create_flavour(
                name, ram, vcpus, disk, swap)
            print(f"flavour_resp: {resp}, flavour_body: {body}")
            flavour_id = body['flavor']['id']
            extra_specs = {
                "powervm:processor_compatibility": "default",
                "powervm:max_vcpu": "3",
                "powervm:min_vcpu": "1",
                "powervm:min_mem": "1024",
                "powervm:max_mem": "4096",
                "powervm:dedicated_proc": "false",
                "powervm:min_proc_units": cls.flavour_min_proc_units,
                "powervm:proc_units": cls.flavour_procunits,
                "powervm:max_proc_units": cls.flavour_max_proc_units,
                "powervm:srr_capability": "false",
                "powervm:enable_lpar_metric": "false",
                "powervm:shared_proc_pool_name": "DefaultPool",
                "powervm:uncapped": "true",
                "powervm:shared_weight": "128",
                "powervm:availability_priority": "127",
                "powervm:secure_boot": "0",
                "powervm:enforce_affinity_check": "false"
            }
            cls.flavors_client.set_flavour_extra_spec(flavour_id, **extra_specs)
            resp, body = cls.flavors_client.list_flavor_extra_specs(flavour_id)
            print(f"List flavor resp: {resp}, body: {body}")
        return flavour_id

    @classmethod
    def _deploy_vms(cls, index, fixed_ip, flavour_id):
        try:
            vm_name='extended-bvt-' + str(index + 1)
            network_id = str(cls.network_client._getNetworkID(cls.network_name))
            network = {
                'fixed_ip': fixed_ip,
                'uuid': network_id
            },
            _, body = cls.os.servers_client.create_vm(
                vm_name, network, flavorRef=flavour_id)
            server_id = body['server']['id']
            time.sleep(600)
            cls.os.servers_client.wait_for_server_with_ping(
                server_id, permissible_statuses=['ACTIVE'],
                permissible_healths=['OK'], network_name=cls.network_name)
            cls.list_of_server_ids.append(server_id)
            print(f"Current list of server ids : {cls.list_of_server_ids} ")
        except Exception as e:
            print(('Something went wrong while waiting for the thread to '
                    'complete: %s' % str(e)))
            cls.resource_cleanup()
            raise

    
    @classmethod
    def _delete_server_with_wait(cls, server_id):
        cls.servers_client.delete_server(server_id)
        waiters.wait_for_server_termination(cls.servers_client,
                                            server_id)
    @classmethod
    def _get_server_ip(cls, server_id):
        ip_value_of_vm = None
        body = cls.servers_client.get_server(server_id)
        print(f"Value of body is of server id : {server_id} is {body}")
        network_addresses=body.get('addresses')
        if network_addresses:
            network_details=network_addresses.get(cls.network_name)
            if len(network_details) > 0:
                network_of_vm=network_details[0]
                ip_value_of_vm=network_of_vm['addr']
                print(f"Value of Ip is {ip_value_of_vm}")
        return ip_value_of_vm

    def create_instance_snapshot(self, ins_snap, isnap_desc, instance_id, volumes = []):
        kwargs = {"name": ins_snap,
                    "description": isnap_desc,
                    "instance_id": instance_id,
                    "volumes": volumes}
        resp, create_inst_snap = self.vm_snapshots_client.create_instance_snapshot(
            **kwargs)
        self.assertEqual(201, resp.status)
        time.sleep(20)
        instSnap_id = create_inst_snap['instance_snapshot']['id']
        return instSnap_id

    def delete_inst_snapshot(self, instSnap_id):
        resp, delete_instance_snapshot = self.vm_snapshots_client.\
            delete_instance_snapshot(instSnap_id)
        time.sleep(20)
        self.assertEqual(202, resp.status)
        resp, inst_snapshot_list = self.vm_snapshots_client.list_instance_snapshot()
        self.assertNotIn(instSnap_id, str(inst_snapshot_list))

    def show_inst_snapshot(self, instSnap_id):
        resp, show_snapshotbody = self.vm_snapshots_client.\
            show_instance_snapshot(instSnap_id)
        time.sleep(20)
        self.assertEqual(200, resp.status)
        return show_snapshotbody

    def list_inst_snapshot(self):
        resp, inst_snapshot_list = self.vm_snapshots_client.\
            list_instance_snapshot()
        time.sleep(20)
        self.assertEqual(200, resp.status)
        return inst_snapshot_list

    def create_vm_snapshot(self, server_id, vm_snap, isnap_desc, volumes = []):
        kwargs = {"name": vm_snap,
                    "description": isnap_desc,
                    "volumes": volumes}
        resp, create_vm_snap = self.servers_client.create_vm_snapshot(server_id, **kwargs)
        self.assertEqual(202, resp.status)
        time.sleep(20)
        instSnap_id = create_vm_snap['instance_snapshot']['id']
        task_uri = create_vm_snap['instance_snapshot']['task_uri']
        return instSnap_id, task_uri

    def _reset_vm_state(self, server_id):
        # Reset the state of vm to Active
        body = self.servers_client.get_server(server_id)
        state = body['status']
        if state == 'ERROR':
            self.servers_client.reset_state(server_id, state="active")
            self.servers_client.wait_for_server_with_ping(
                server_id,
                permissible_statuses=['ACTIVE'],
                permissible_healths=[
                    'OK',
                    'WARNING'],
                    network_name=self.network_name)

    def _raise_exception_for_no_vms(self):
        if len(self.list_of_server_ids) == 0:
            msg = "No VMs exist. Raising exception."
            raise Exception(msg)
        
    @classmethod
    def _cleanup_cpn(cls):
        _, resp = cls.cpn_client.list_cpn()
        cpns = resp['compute_planes']
        for cpn in cpns:
            _, resp = cls.cpn_client.deregister_cpn(cpn['id'])

    def _register_cpn(self, cpn):
        _, resp = self.cpn_client.register_cpn(
            display_name=cpn['display_name'],
            access_ip=cpn['access_ip'],
            user_id=cpn['user_id'],
            password=cpn['password'])
        time.sleep(120)
        resp_cpn = resp['compute_plane']['registration']
        self.assertEqual(cpn['display_name'], resp_cpn['display_name'])
        self.assertEqual(cpn['access_ip'], resp_cpn['access_ip'])
        self.assertEqual(cpn['user_id'], resp_cpn['user_id'])
        self.cpn_client.wait_for_cpn_health(cpn['display_name'])
        return resp_cpn['id']

    def test_001_attach_detach_active_vm(self):
        self._raise_exception_for_no_vms()
        server_id = self.list_of_server_ids[0]
        print(f"server_id {server_id}")
        exist_volume3 = data_utils.rand_name("exist_volume")
        exist_volume4 = data_utils.rand_name("exist_volume")
        time.sleep(50)
        # resp, body2 = self.volume_client.get_volume_templates_list()
        base_template_name = self.os.config.volume.host_name + " base template"
        base_template_id = self.volume_types_v3_client.get_volume_template_id(base_template_name)
        print(f"base_template_id: {base_template_id}")
        time.sleep(50)
        # dict_multiattach = {"volume_type": base_template_id}
        print(f"self.volume_client: {self.volumes_v3_client}  \n locals: {locals()}")
        self.volumes_v3_client.create_volume(name=exist_volume3, size=1, volume_type=base_template_id)
        print(f"Volume {exist_volume3} created triggered") 
        self.volumes_v3_client.create_volume(name=exist_volume4, size=1, volume_type=base_template_id)
        print(f"Volume {exist_volume4} created triggered")
        volume_id = self.volume_client.get_volume_id(exist_volume3)
        print(f"volume_id {volume_id}")
        time.sleep(50)
        self.addCleanup(self.os.volume_client.delete_volume,
                        volume_id)
        print(f"Added {volume_id} for cleanup. Waiting for {volume_id} to become available")
        self.volume_client.wait_for_volume_status(volume_id, "available")
        vol_id4 = self.volume_client.get_volume_id(exist_volume4)
        print(f"vol_id4 {vol_id4}")
        self.addCleanup(self.os.volume_client.delete_volume,
                        vol_id4)
        print(f"Added {vol_id4} for cleanup. Waiting for {vol_id4} to become available")
        self.volume_client.wait_for_volume_status(vol_id4, "available")
        print(f"Attaching volume: {volume_id} to instance: {server_id}")
        volume_id_meta= {
             "volumeId": volume_id,
             "is_boot_volume": "False",
             "device": None
         }
        self.servers_client.bulk_volume_attachment(server_id, [volume_id_meta])
        print(f"Waiting for Attaching volume to complete for volume {volume_id}")
        self.volume_client.wait_for_volume_status(volume_id, "in-use")
        time.sleep(50)
        print(f"Attaching volume: {vol_id4} to instance: {vol_id4}")
        vol_id4_meta = {
             "volumeId": vol_id4,
             "is_boot_volume": "False",
             "device": None
         }
        self.servers_client.bulk_volume_attachment(server_id, [vol_id4_meta])
        print(f"Waiting for Attaching volume to complete for volume {vol_id4}")
        self.volume_client.wait_for_volume_status(vol_id4, "in-use")
        print(f"Detaching volume: {volume_id} from instance: {server_id}")
        self.servers_client.delete_volume_attachments_by_id(server_id, volume_id)
        print(f"Waiting for detaching volume to complete for volume {volume_id}")
        self.volume_client.wait_for_volume_status(volume_id, "available")
        print(f"Detaching volume: {vol_id4} from instance: {server_id}")
        self.servers_client.delete_volume_attachments_by_id(server_id, vol_id4)
        print(f"Waiting for detaching volume to complete for volume {vol_id4}")
        self.volume_client.wait_for_volume_status(vol_id4, "available")
        time.sleep(100)

    def test_002_capture_image_on_active_vm(self):
        time.sleep(30)
        self._raise_exception_for_no_vms()
        server_id = self.list_of_server_ids[1]
        time.sleep(30)
        self.servers_client.wait_for_server_with_ping(
            server_id, network_name=self.network_name)
        server = self.servers_client.get_server(server_id)
        server_image = data_utils.rand_name("image-lifecycle")
        if server['status'] == 'ACTIVE':
            body = self.images_client.create_image(server_id, name=server_image)
            print(f"Result of create image is : {body}")
            time.sleep(100)
            image_id = self.image_client_v2._get_image_id(server_image)
            print(f"Value of image ID is : {image_id}")
            self.image_client_v2.wait_for_image_status(image_id, "active")
            time.sleep(30)
            self.image_client_v2.delete_image_from_capture(
                image_id, self.os.volume_client)
        else:
            msg = ("The value of server status is"
                   " :%s.Please make sure VM is in "
                   "status 'OK'" % server['status']) 
            raise Exception(msg)


    def test_003_resize_server_active(self):
        time.sleep(30)
        self._raise_exception_for_no_vms()
        time.sleep(30)
        server_id = self.list_of_server_ids[2]
        __,body_flavour = self.flavors_client.show_flavor_extra_spec(self.flavour_id)
        print(f"The value of extra-specs {body_flavour}")
        body_flavour['extra_specs'].update({'powervm:proc_units':'0.06'})
        print(f"The value of updated extra-specs {body_flavour}")
        body = self.servers_client.get_server(server_id)
        print(f"The value of get servers {body}")
        self.servers_client.wait_for_server_with_ping(
            server_id, "OK", network_name=self.network_name)
        resize_dict = {"flavor":
                       {"vcpus": int(body["cpus"]),
                        "ram": int(body["memory_mb"] * 2),
                        "disk": int(body["root_gb"]),
                        "extra_specs": body_flavour['extra_specs']
                        }}
        print(f"The value of resize dict {resize_dict}")
        if ((body['status'] == "ACTIVE") and
                (body['health_status']['health_value'] in (
                    "OK"))):
            time.sleep(30)
            self.servers_client.resize(server_id, **resize_dict)
            time.sleep(100)
            self.servers_client.wait_for_server_with_ping(
                server_id,
                permissible_statuses=['ACTIVE'],
                permissible_healths=['OK'], network_name=self.network_name)
        else:
            self.assertFalse(
                True,
                "failed to resize as server doesnot meet requirement")
        server_body = self.servers_client.get_server(server_id)
        state = server_body['status']
        if state == 'ERROR':
            time.sleep(30)
            self._reset_vm_state(server_id)
        self.assertEqual(server_body['memory_mb'],
                         resize_dict["flavor"]["ram"])


    def test_004_attach_detach_inactive_vm(self):
        time.sleep(30)
        self._raise_exception_for_no_vms()
        server_id = self.list_of_server_ids[3]
        print(f"server_id {server_id}")
        self.servers_client.stop_server(server_id)
        waiters.wait_for_server_status(self.servers_client,
                                       server_id, 'SHUTOFF')
        exist_volume3 = data_utils.rand_name("exist_volume")
        exist_volume4 = data_utils.rand_name("exist_volume")
        base_template_name = self.os.config.volume.host_name + " base template"
        base_template_id = self.volume_types_v3_client.get_volume_template_id(base_template_name)
        print(f"base_template_id: {base_template_id}")
        # dict_multiattach = {"volume_type": base_template_id}
        print(f"self.volume_client: {self.volumes_v3_client}  \n locals: {locals()}")
        self.volumes_v3_client.create_volume(name=exist_volume3, size=1, volume_type=base_template_id)
        print(f"Volume {exist_volume3} created triggered") 
        self.volumes_v3_client.create_volume(name=exist_volume4, size=1, volume_type=base_template_id)
        print(f"Volume {exist_volume4} created triggered")
        volume_id = self.volume_client.get_volume_id(exist_volume3)
        print(f"volume_id {volume_id}")
        self.addCleanup(self.os.volume_client.delete_volume,
                        volume_id)
        print(f"Added {volume_id} for cleanup. Waiting for {volume_id} to become available")
        self.volume_client.wait_for_volume_status(volume_id, "available")
        vol_id4 = self.volume_client.get_volume_id(exist_volume4)
        print(f"vol_id4 {vol_id4}")
        self.addCleanup(self.os.volume_client.delete_volume,
                        vol_id4)
        print(f"Added {vol_id4} for cleanup. Waiting for {vol_id4} to become available")
        self.volume_client.wait_for_volume_status(vol_id4, "available")
        print(f"Attaching volume: {volume_id} to instance: {server_id}")
        volume_id_meta= {
             "volumeId": volume_id,
             "is_boot_volume": "False",
             "device": None
         }
        self.servers_client.bulk_volume_attachment(server_id, [volume_id_meta])
        print(f"Waiting for Attaching volume to complete for volume {volume_id}")
        self.volume_client.wait_for_volume_status(volume_id, "in-use")
        time.sleep(50)
        print(f"Attaching volume: {vol_id4} to instance: {vol_id4}")
        vol_id4_meta = {
             "volumeId": vol_id4,
             "is_boot_volume": "False",
             "device": None
         }
        self.servers_client.bulk_volume_attachment(server_id, [vol_id4_meta])
        print(f"Waiting for Attaching volume to complete for volume {vol_id4}")
        self.volume_client.wait_for_volume_status(vol_id4, "in-use")
        time.sleep(50)
        print(f"Detaching volume: {volume_id} from instance: {server_id}")
        self.servers_client.delete_volume_attachments_by_id(server_id, volume_id)
        print(f"Waiting for detaching volume to complete for volume {volume_id}")
        self.volume_client.wait_for_volume_status(volume_id, "available")
        print(f"Detaching volume: {vol_id4} from instance: {server_id}")
        self.servers_client.delete_volume_attachments_by_id(server_id, vol_id4)
        print(f"Waiting for detaching volume to complete for volume {vol_id4}")
        self.volume_client.wait_for_volume_status(vol_id4, "available")
        body = self.servers_client.get_server(server_id)
        if body['status'] == 'SHUTOFF':
            self.servers_client.start_server(server_id)
            self.servers_client.wait_for_server_with_ping(server_id,
                    permissible_statuses=['ACTIVE'],
                    permissible_healths=['OK'], network_name=self.network_name)

    def test_005_capture_image_on_inactive_vm(self):
        time.sleep(30)
        self._raise_exception_for_no_vms()
        server_id = self.list_of_server_ids[4]
        time.sleep(30)
        self.servers_client.wait_for_server_with_ping(
            server_id, network_name=self.network_name)
        server = self.servers_client.get_server(server_id)
        server_image = data_utils.rand_name("image-lifecycle")
        if server['status'] == 'ACTIVE':
            self.servers_client.stop_server(server_id)
            time.sleep(30)
            waiters.wait_for_server_status(self.servers_client,
                                        server_id, 'SHUTOFF')
            self.servers_client.wait_for_server_health_status(server_id, "OK")
        server = self.servers_client.get_server(server_id)
        self.images_client.create_image(server_id, name=server_image)
        time.sleep(30)
        image_id = self.image_client_v2._get_image_id(server_image)
        self.image_client_v2.wait_for_image_status(image_id, "active")
        time.sleep(30)
        self.image_client_v2.delete_image_from_capture(
            image_id, self.os.volume_client)
        body = self.servers_client.get_server(server_id)
        if body['status'] == 'SHUTOFF':
            self.servers_client.start_server(server_id)
            time.sleep(100)
            self.servers_client.wait_for_server_with_ping(server_id,
                    permissible_statuses=['ACTIVE'],
                    permissible_healths=['OK'], network_name=self.network_name)

    def test_006_stop_start_server(self):
        time.sleep(30)
        self._raise_exception_for_no_vms()
        time.sleep(30)
        server_id = self.list_of_server_ids[1]
        vm_ip = self._get_server_ip(server_id)
        body = self.servers_client.get_server(server_id)
        if body['status'] == 'SHUTOFF':
            self.servers_client.start_server(server_id)
            try:
                self.servers_client.wait_for_server_with_ping(
                    server_id, network_name=self.network_name)
            except Exception as e:
                print(('Something went wrong while waiting for the server to '
                       'come up: %s' % str(e)))
        body = self.servers_client.get_server(server_id)
        self.servers_client.wait_for_server_with_ping(
            server_id, network_name=self.network_name)
        self.servers_client.stop_server(server_id)
        time.sleep(30)
        waiters.wait_for_server_status(self.servers_client,
                                       server_id, 'SHUTOFF')
        time.sleep(50)
        if vm_ip and self.servers_client.ping_test_vm_ip(vm_ip) is False:
            self.servers_client.wait_for_server_health_status(server_id, "OK")
        else:
            pass
        self.servers_client.start_server(server_id)
        try:
            time.sleep(100)
            if vm_ip and self.servers_client.ping_test_vm_ip(vm_ip) is False:
                self.servers_client.wait_for_server_with_ping(
                    server_id, network_name=self.network_name)
            else:
                pass
        except Exception as e:
            print(('Something went wrong while waiting for the server to '
                   'come up: %s' % str(e)))
            pass

    def test_008_hard_restart_server(self):
        time.sleep(30)
        self._raise_exception_for_no_vms()
        time.sleep(30)
        server_id = self.list_of_server_ids[2]
        self.servers_client.restart(server_id, rtype='HARD')
        """the server comes in OK state straightaway so sleep"""
        time.sleep(180)
        self.servers_client.wait_for_server_with_ping(
                server_id, network_name=self.network_name)

    def test_009_clone_vm_active_ok_default_group(self):
        time.sleep(30)
        self._raise_exception_for_no_vms()
        fixed_ip = self.os.config.network.network_fixed_ip6
        vm_id = self.list_of_server_ids[0]
        kwargs = {"availability_zone":  "Default Group"}
        networks = []
        network_id = str(self.network_client._getNetworkID(self.network_name))
        networks.append({'uuid': network_id, 'fixed_ip': fixed_ip})
        clone_vm_name = data_utils.rand_name("active-OK-vm-clone" + vm_id)
        resp, body = self.servers_client.clone_vm(vm_id,
                                                    clone_vm_name,
                                                    networks, **kwargs)
        self.assertEqual(202, resp.status)
        time.sleep(150)
        self.clone_server_id = self.servers_client.get_server_id(clone_vm_name)
        self.servers_client.wait_for_server_with_ping(
            self.clone_server_id,
            permissible_statuses=['ACTIVE'],
            permissible_healths=['OK','WARNING'], network_name=self.network_name)
        time.sleep(30)
        self.servers_client.delete_server(self.clone_server_id)
        time.sleep(100)
        
    def test_012_clone_vm_inactive_ok_default_group(self):
        time.sleep(30)
        self._raise_exception_for_no_vms()
        time.sleep(60)
        fixed_ip = self.os.config.network.network_fixed_ip6
        vm_id = self.list_of_server_ids[3]
        self.servers_client.stop_server(vm_id)
        waiters.wait_for_server_status(self.servers_client,
                                   vm_id, 'SHUTOFF')
        self.servers_client.wait_for_server_with_ping(
            vm_id, permissible_statuses=["SHUTOFF"], permissible_healths=["OK"],
            network_name=self.network_name)
        kwargs = {"availability_zone":  "Default Group"}
        networks = []
        network_id = str(self.network_client._getNetworkID(self.network_name))
        networks.append({'uuid': network_id, 'fixed_ip': fixed_ip})
        clone_vm_name = data_utils.rand_name("active-OK-vm-clone" + vm_id)
        resp, body = self.servers_client.clone_vm(vm_id,
                                                    clone_vm_name,
                                                    networks, **kwargs)
        self.assertEqual(202, resp.status)
        time.sleep(150)
        self.clone_server_id = self.servers_client.get_server_id(clone_vm_name)
        self.servers_client.wait_for_server_with_ping(
            self.clone_server_id,
            permissible_statuses=['ACTIVE'],
            permissible_healths=['OK','WARNING'], network_name=self.network_name)
        self.servers_client.delete_server(self.clone_server_id)
        time.sleep(100)
        body = self.servers_client.get_server(vm_id)
        if body['status'] == 'SHUTOFF':
            self.servers_client.start_server(vm_id)
            time.sleep(100)
            self.servers_client.wait_for_server_with_ping(vm_id,
                    permissible_statuses=['ACTIVE'],
                    permissible_healths=['OK'], network_name=self.network_name)

    def test_011_compute_host_unonboard_onboard_VM(self):
        time.sleep(60)
        self._raise_exception_for_no_vms()
        server_id = self.list_of_server_ids[4]
        body = self.servers_client.get_server(server_id)
        body1 = self.servers_client.list_servers()
        print(f"Value of list servers is : {body1}")
        for vm_detail in body1['servers']:
            for key, value in vm_detail.items():
                if value == server_id:
                    vm_name = vm_detail['name']
                    break
        deployed_host = body["OS-EXT-SRV-ATTR:host"]
        resp, body = self.compute_client.compute_host_unonboard_particularVM(
            deployed_host, [server_id])
        self.assertEqual(204, resp.status)
        resp, body = self.compute_client.list_onboarding_Existing_compute_host(
            deployed_host)
        print(f"Response of listing VM to onboard {body}" )
        self.assertEqual(200, resp.status)
        hypervisor_body = body
        print(f"The hypervisor body is : {hypervisor_body}")
        hypervisor_host = deployed_host
        print(f"The hypervisor host is : {hypervisor_host}")
        vm_id = None
        found_vm_on_host = False
        for entry in hypervisor_body:
            str_vm = str(entry)
            if str_vm.find(vm_name) > 0:
                vm_id = entry['id']
                vm_name_onboarded = entry['name']
                print(f"vm_id: {vm_id} onboarded : {vm_name_onboarded}")
                found_vm_on_host = True
                break
        if found_vm_on_host:
            resp, body = self.compute_client.compute_host_onboard_particularVM(
                deployed_host, vm_id)
            self.assertEqual('200', resp['status'])
            body2 = self.servers_client.list_servers()
            start = int(time.time())
            while (vm_name_onboarded not in str(body2)):
                time.sleep(10)
                body2 = self.servers_client.list_servers()
                if int(time.time()) - start >= 200:
                    message = (
                        'VM-ID %s is intiated but failed to \
                        onboard within the required time (%s s).' %
                        (vm_id, 200))
                    raise Exception(message)
        else:
            print(f"Not able to find VM: {vm_name} on the host.")

    def test_010_list_servers_with_detail(self):
        time.sleep(30)
        self.servers_client.list_servers(detail=True)

    def test_013_get_server_by_id(self):
        time.sleep(30)
        self._raise_exception_for_no_vms()
        server_id = self.list_of_server_ids[0]
        time.sleep(30)
        body = self.servers_client.get_server(server_id)
        self.assertEqual(body['id'], server_id)

    def test_014_instance_snapshot(self):
        time.sleep(30)
        # create instance snapshot
        self._raise_exception_for_no_vms()
        server_id = self.list_of_server_ids[1]
        resp, body = self.servers_client.get_server_os_volume_attachment(
            server_id)
        print(f"test_014_instance_snapshot: get_server_os_volume_attachment"
              f"resp: {resp}, body: {body}")
        body = body['server'] if body.get('server') else body
        print(f"test_014_instance_snapshot: next body:{body}")
        details_of_vol_attachment = body['volumeAttachments']
        print(f"test_014_instance_snapshot: details_of_vol_"
              f"attachment:{details_of_vol_attachment}")
        volume_id = details_of_vol_attachment[0]['volumeId']
        inst_snap_id = self.create_instance_snapshot(
            "extended_bvt_test_instance_snapshot",
            "Instance-Snapshot using instance snapshot API",
            server_id, [volume_id])
        print(f"Instance snapshot is taken successfully, Id {inst_snap_id}")
        # list snapshot details
        snapshot_list = self.list_inst_snapshot()
        self.assertIn(inst_snap_id, str(snapshot_list))
        # get snapshot details
        show_snapshotbody = self.show_inst_snapshot(inst_snap_id)
        print(f"test_014_instance_snapshot: show_snapshotbody"
              f":{show_snapshotbody}")
        self.assertEqual(str(show_snapshotbody['instance_snapshot']['id']),
                                inst_snap_id)
        self.assertIn(volume_id, str(show_snapshotbody['instance_snapshot']))
        # delete instance snapshot
        self.delete_inst_snapshot(inst_snap_id)

    def test_015_vm_snapshot(self):
        time.sleep(30)
        self._raise_exception_for_no_vms()
        # create vm snapshot
        server_id = self.list_of_server_ids[2]
        resp, body = self.servers_client.get_server_os_volume_attachment(
            server_id)
        print(f"test_015_vm_snapshot: get_server_os_volume_attachment"
              f"resp: {resp}, body: {body}")
        body = body['server'] if body.get('server') else body
        print(f"test_015_vm_snapshot: next body:{body}")
        details_of_vol_attachment = body['volumeAttachments']
        volume_id = details_of_vol_attachment[0]['volumeId']
        inst_snap_id, task_uri = self.create_vm_snapshot(
            server_id, "extended_bvt_test_vm_snapshot",
            "VM Snapshot", [volume_id])
        print("VM snapshot is taken successfully and Id : %s" %inst_snap_id)
        # Validate the Task progress
        resp, task = self.vm_snapshots_client.get_task_progress(task_uri.split("instance-snapshots")[1])
        self.assertEqual(200, resp.status)
        self.assertEqual(100, task['details']['progress'])
        # delete vm snapshot
        self.delete_inst_snapshot(inst_snap_id)
    
    @classmethod
    def update_cleanup_all_resources_value(cls, value):
        cls.cleanup_all_resources = value

    def test_016_cleanup_all_resources(self):
        self.update_cleanup_all_resources_value("true")

    def test_007_resize_server_inactive(self):
        self._raise_exception_for_no_vms()
        time.sleep(100)
        server_id = self.list_of_server_ids[0]
        __,body_flavour = self.flavors_client.show_flavor_extra_spec(
            self.flavour_id)
        print(f"The value of extra-specs {body_flavour}")
        body_flavour['extra_specs'].update({'powervm:proc_units':'0.06'})
        print(f"The value of updated extra-specs {body_flavour}")
        body = self.servers_client.get_server(server_id)
        print(f"The value of get servers {body}")
        self.servers_client.wait_for_server_with_ping(
            server_id, "OK", network_name=self.network_name)
        resize_dict = {"flavor":
                       {"vcpus": int(body["cpus"]),
                        "ram": int(body["memory_mb"] * 2),
                        "disk": int(body["root_gb"]),
                        "extra_specs": body_flavour['extra_specs']
                        }}
        print(f"The value of resize dict {resize_dict}")
        if ((body['status'] == "ACTIVE") and
                (body['health_status']['health_value'] in (
                    "OK"))):
            self.servers_client.stop_server(server_id)
            time.sleep(100)
            waiters.wait_for_server_status(self.servers_client,
                                        server_id, 'SHUTOFF')
            self.servers_client.wait_for_server_health_status(server_id, "OK")
            time.sleep(100)
            self.servers_client.resize(server_id, **resize_dict)
            time.sleep(200)
            self.servers_client.wait_for_server_with_ping(server_id,
                                                permissible_statuses=['SHUTOFF'],
                                                permissible_healths=['OK', 'WARNING'],
                                                network_name=self.network_name)
        server_body = self.servers_client.get_server(server_id)
        state = server_body['status']
        if state == 'ERROR':
            self._reset_vm_state(server_id)
            self.assertEqual(server_body['memory_mb'],
                         resize_dict["flavor"]["ram"])
        if state == 'SHUTOFF':
            self.servers_client.start_server(server_id)
            time.sleep(100)
            self.servers_client.wait_for_server_with_ping(server_id,
                    permissible_statuses=['ACTIVE'],
                    permissible_healths=['OK'],
                    network_name=self.network_name)
            

               
    def _get_compute_hostnames(self):
        body = self.hosts_client.list_hosts()['hosts']
        return [
            host_record['host_name']
            for host_record in body
            if host_record['service'] == 'compute'
        ]

            
    def _get_server_details(self, server_id):
        body = self.servers_client.show_server(server_id)['server']
        return body
            
    def _get_host_for_server(self, server_id):
        return self._get_server_details(server_id)["OS-EXT-SRV-ATTR:host"]
    
    def _get_host_other_than(self, host):
        for target_host in self._get_compute_hostnames():
            if host != target_host:
                return target_host
                
            
    def test_000_migrate_server(self):
        self._raise_exception_for_no_vms()
        time.sleep(30)
        print("Entering Migration Test")
        # Migration test
        print(f"Number of hosts : {len(self._get_compute_hostnames())}")
        if len(self._get_compute_hostnames()) < 2:
            raise self.skipTest(
                "Less than 2 compute nodes, skipping migration test.")
        server_id = self.list_of_server_ids[0]
        print(f"Performing Migration on : {server_id}")
        body = self.servers_client.get_server(server_id)
        print(f"Performing Migration get server : {body}")
        if body['status'] == 'SHUTOFF':
            self.servers_client.start_server(server_id)
        self.servers_client.wait_for_server(server_id)
        body = self.servers_client.get_server(server_id)
        state = body['status']
        print(f"State of VM on which migration is to be performed: {state}")
        self.assertEqual(state,
                         "ACTIVE",
                         "state of the machine is not active and health: %s"
                         % body['health_status']['health_value'])
        # Untargetted migration
        actual_host = self._get_host_for_server(server_id)
        print(f"actual_host of VM on which migration is to be performed: {actual_host}")
        migrated_to_host = self._get_host_other_than(actual_host)
        print(f"migrated_to_host of VM on which migration is to be performed: {migrated_to_host}")
        body = self.servers_client.live_migrate_server(
            server_id, host=None,
            block_migration=False,
            disk_over_commit=False)

        print(f"output after VM migration body: {body}")

        self.servers_client.wait_for_server(
            server_id,
            permissible_statuses=['ACTIVE'],
            permissible_healths=['OK']
            )

        self.assertNotEqual(actual_host, self._get_host_for_server(server_id),
                            "Migration Failed as VM still on actual host")

        body = self.servers_client.get_server(server_id)
        print(f"After Performing Migration get server : {body}")
        state = body['status']
        if state == 'ERROR':
            self._reset_vm_state(server_id)
            self.assertEqual(state,
                             "ACTIVE"
                             "VM migrated but went to error because %s "
                             % body["fault"]["message"])
        # targetted migration
        # Logic for waiting for rmc state to be active before migration:
        time.sleep(200)
        print("Starting targetted Migration get server")
        self.servers_client.wait_for_server_health_status(server_id, "OK")
#        self._wait_for_rmc_status_active(migrated_to_host, server_id)
        actual_host = self._get_host_for_server(server_id)
        target_host = self._get_host_other_than(actual_host)
        time.sleep(200)
        body = self.servers_client.live_migrate_server(
            server_id, host=target_host,
            block_migration=False,
            disk_over_commit=False)
        print(f"Body after targetted Migration get server {body}")
        self.servers_client.wait_for_server(
            server_id,
            permissible_statuses=['ACTIVE'],
            permissible_healths=['OK'])
        self.assertNotEqual(actual_host,
                            target_host,
                            "Migration Failed as VM still on actual host")
        body = self.servers_client.get_server(server_id)
        state = body['status']
        if state == 'ERROR':
            self._reset_vm_state(server_id)
            self.assertEqual(state,
                             "ACTIVE"
                             "VM migrated but went to error because %s "
                             % body["fault"]["message"])
            
    def test_017_register_cpn_n_detail(self):
        self._cleanup_cpn()
        for cpn in self.compute_plane_node_list:
            self._register_cpn(cpn)
        _, resp = self.cpn_client.list_cpn()
        cpns = resp['compute_planes']
        self.assertEqual(len(cpns), len(self.compute_plane_node_list))
        for cpn in cpns:
            _, resp = self.cpn_client.show_cpn(cpn['id'])
            resp_cpn = resp['compute_plane']
            self.assertEqual(cpn['display_name'], resp_cpn['display_name'])
            self.assertEqual(cpn['access_ip'], resp_cpn['access_ip'])
            self.assertEqual(cpn['user_id'], resp_cpn['user_id'])
            self.assertEqual(cpn['id'], resp_cpn['id'])

    @classmethod
    def _hardwarecleanup(cls):
        print(f"_hardwarecleanup called from fvt_test_lifecycle.py")
        pass

    @classmethod
    def _delete_vm(cls, server_id):
        print(f"Deleting server: {server_id}")
        try:
            cls.os.servers_client.delete_server(server_id)
            waiters.wait_for_server_termination(cls.os.servers_client,
                                                server_id,
                                                ignore_error=True)
        except BaseException:
            print(f'Failed to delete server: {server_id} in FVTLifecycle')
            pass

    @classmethod
    def _delete_ports(cls):
        delete_port_list = []
        body = cls.os.ports_client.list_ports()
        for ports in body["ports"]:
            if ports["device_id"] == "":
                delete_port_list.append(ports["id"])
        for port in delete_port_list:
            try:
                cls.os.ports_client.delete_port(port)
            except BaseException:
                print('Failed to delete port in NetworkPortID')
                pass

    @classmethod
    def resource_cleanup(cls):
        print(f"cls.cleanup_all_resources: {cls.cleanup_all_resources}")
        if cls.cleanup_all_resources.lower() == "true":
            vm_delete_threads = []
            cls.list_of_server_ids = cls._get_server_ids()
            if len(cls.list_of_server_ids) > 0:
                for server_id in cls.list_of_server_ids:
                    vm_delete_thread = threading.Thread(target=cls._delete_vm, args=(server_id,))
                    vm_delete_threads.append(vm_delete_thread)
                    vm_delete_thread.start()

            for vm_delete_thread in vm_delete_threads:
                try:
                    vm_delete_thread.join()
                except Exception as e:
                    print(('Something went wrong while waiting for the vm_delete thread to '
                        'complete: %s' % str(e)))
                    pass
            
            try:
                print("Trying to delete ports")
                cls._delete_ports()
            except Exception as ex1:
                print("Exception in _delete_ports in FVTLifecycle: {ex}")
                pass
                    
            try:
                cls.os.flavors_client.delete_flavor(cls.flavour_id)
            except BaseException:
                print('Failed to delete flavor in DeployWithExtraSpecTests')
            pass
            
        print(f"Calling super class's"
              f" resource_cleanup for FVTLifecycle")
        try:
            cls._cleanup_cpn()
        except BaseException:
            print('CPN removal operation failed in CPNTests')
        try:
            super(FVTLifecycle, cls).resource_cleanup()
        except BaseException:
            print('Deletion failed in FVTLifecycle')
            pass
        except Exception as ex:
            print("Exception in resource_cleanup in FVTLifecycle: {ex}")
            pass
