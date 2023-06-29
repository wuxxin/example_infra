def provision_remote_port_url():
    from infra.tools import get_default_host_ip

    local_port = 4711
    remote_url = "https://{ip}:{port}/".format(ip=get_default_host_ip(), port=local_port)
    return local_port, remote_url


def provision_image():
    "prepare an image for transfer to sdcard / usbstick"

    import infra.build
    import infra.fcos
    from target.safe import shortname, hostname
    from infra.tools import public_local_export

    local_port, remote_url = provision_remote_port_url()
    public_ign = infra.fcos.RemoteDownloadIgnitionConfig(
        "{}_public_ignition".format(shortname), hostname, remote_url
    )

    # build image to copy on sdcard
    machine = {
        "extras": infra.build.build_raspberry(),
        "image": infra.fcos.FcosImageDownloader(architecture="aarch64"),
        "config": public_local_export(
            shortname, "{}_public.ign".format(shortname), public_ign.result
        ),
    }


def secure_provision_ignition():
    import infra.authority as authority
    import target.safe as safe
    from target.safe import shortname, hostname
    from infra.tools import ServeOnce

    local_port, remote_url = provision_remote_port_url()

    # serve secret part of ign via serve_once and mandatory client certificate
    serve_config = {
        "serve_port": local_port,
        "timeout": 45,
        "cert": authority.provision_host_tls.chain,
        "key": authority.provision_host_tls.key.private_key_pem,
        "ca_cert": authority.ca_factory.root_cert_pem,
        "mtls": True,
        "payload": safe.butane_yaml.ignition_config,
    }
    secret_ignition_served = ServeOnce(
        "serve_public_ign_for_{}".format(shortname), serve_config
    )
