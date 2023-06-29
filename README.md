# example_infra

Software Defined Git Operated Infrastructure as Code

ShowCase of https://github.com/wuxxin/infra-shared

**Work In Progress** 

## Safe - Fedora-CoreOS on ARM

- Minimum Viable Function
    - encrypted storage at rest
    - unattended update/boot
        - unattended clevis luks storage unlock via tangd (and tpm2 on libvirt sim)
    - postgresql database for storing data

- Hardware: Raspberry Pi4
    - sdcard with boot and luks encrypted root
    - 2 x usb sticks: luks encrypted raid1 mirrored /var

- Single Container
    - postgresql - with mandatory ssl and optional clientcert auth

- Simulation
    - a libvirt machine with the corresponding features and volumes


- Additional
    - compose hello-compose Application
    - nspawn hello-nspawn Application
 