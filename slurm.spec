Name:		slurm
Version:	14.03.8
Release:	1%{?dist}
Summary:	Simple LinUx Resource Manager

Group:		System Environment/Base
License:	GPLv2
URL:		http://www.schedmd.com
Source0:	http://www.schedmd.com/download/latest/%{name}-%{version}.tar.bz2
Source1:	slurmd.service
Source2:	slurmctld.service
Source3:	slurmdbd.service

BuildRequires:	python, gtk2-devel, ncurses-devel, readline-devel, openssl-devel
BuildRequires:	mysql-devel, numactl-devel, hwloc-devel, hdf5-devel, libtool
BuildRequires:	perl(ExtUtils::MakeMaker), freeipmi-devel, autoconf, automake
BuildRequires:	munge-devel, lua-devel, pam-devel, rrdtool-devel, m4
%if 0
BuildRequires:	libumad-devel, libmad-devel
%endif

%if 0%{?fedora} > 15
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%else
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts
%endif

%description
Slurm is an open source, fault-tolerant, and highly
scalable cluster management and job scheduling system for Linux clusters.
Components include machine status, partition management, job management,
scheduling and accounting modules

%package devel
Summary: Development package for Slurm
Group: Development/System
Requires: slurm
%description devel
Development package for Slurm.  This package includes the header files
and static libraries for the Slurm API

%package auth-none
Summary: Slurm auth NULL implementation (no authentication)
Group: System Environment/Base
Requires: slurm
%description auth-none
Slurm NULL authentication module

%package munge
Summary: Slurm authentication and crypto implementation using Munge
Group: System Environment/Base
Requires: slurm munge
BuildRequires: munge-devel munge-libs
%description munge
Slurm authentication and crypto implementation using Munge. Used to
authenticate user originating an RPC, digitally sign and/or encrypt messages

%package pam_slurm
Summary: PAM module for restricting access to compute nodes via Slurm
Group: System Environment/Base
Requires: slurm slurm-devel
BuildRequires: pam-devel
%description pam_slurm
This module restricts access to compute nodes in a cluster where Slurm is in
use.  Access is granted to root, any user with an Slurm-launched job currently
running on the node, or any user who has allocated resources on the node
according to the Slurm

%package perlapi
Summary: Perl API to Slurm
Group: Development/System
Requires: slurm
%description perlapi
Perl API package for Slurm.  This package includes the perl API to provide a
helpful interface to Slurm through Perl

%package plugins
Summary: Slurm plugins (loadable shared objects)
Group: System Environment/Base
%description plugins
Slurm plugins (loadable shared objects) supporting a wide variety of
architectures and behaviors. These basically provide the building blocks
with which Slurm can be configured. Note that some system specific plugins
are in other packages

%package sjobexit
Summary: Slurm job exit code management tools
Group: Development/System
Requires: slurm-perlapi
%description sjobexit
Slurm job exit code management tools. Enables users to alter job exit code
information for completed jobs

%package sjstat
Summary: Perl tool to print Slurm job state information
Group: Development/System
Requires: slurm
%description sjstat
Perl tool to print Slurm job state information. The output is designed to give
information on the resource usage and availablilty, as well as information
about jobs that are currently active on the machine. This output is built
using the Slurm utilities, sinfo, squeue and scontrol, the man pages for these
utilites will provide more information and greater depth of understanding

%package slurmdbd
Summary: Slurm database daemon
Group: System Environment/Base
Requires: slurm-plugins slurm-sql
%description slurmdbd
Slurm database daemon. Used to accept and process database RPCs and upload
database changes to slurmctld daemons on each cluster

%package slurmdb-direct
Summary: Wrappers to write directly to the slurmdb
Group: Development/System
Requires: slurm-perlapi
%description slurmdb-direct
Wrappers to write directly to the slurmdb

%package sql
Summary: Slurm SQL support
Group: System Environment/Base
%description sql
Slurm SQL support. Contains interfaces to MySQL.

%package torque
Summary: Torque/PBS wrappers for transitition from Torque/PBS to Slurm
Group: Development/System
Requires: slurm-perlapi
%description torque
Torque wrapper scripts used for helping migrate from Torque/PBS to Slurm

%package lua
Summary: Slurm lua bindings
Group: System Environment/Base
Requires: slurm lua
BuildRequires: lua-devel
%description lua
Slurm lua bindings
Includes the Slurm proctrack/lua and job_submit/lua plugin

%{!?_slurm_sysconfdir: %global _slurm_sysconfdir /etc/slurm}
%define _sysconfdir %_slurm_sysconfdir

%prep
%setup -q


%build
for x in auxdir/*.m4 ; do
  sed -i 's/-Wl,-rpath -Wl,[^ ]* //' $x
done
autoreconf
%configure \
  --with-ssl \
  --with-munge \
  --enable-shared \
  --disable-static \
  --with-rrdtool \
  --with-hdf5 \
  --with-freeipmi \
  --without-rpath
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
make install-contrib DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{perl_vendorarch}
mv %{buildroot}%{_libdir}/perl5/S* %{buildroot}%{perl_vendorarch}/
mv %{buildroot}%{_libdir}/perl5/auto %{buildroot}%{perl_vendorarch}/
mv %{buildroot}%{_libdir}/perl5/config* %{buildroot}%{perl_vendorarch}/
%if 0%{?fedora} > 15
mkdir -vp %{buildroot}%{_unitdir}
install -m 644 -p %{SOURCE1} %{buildroot}%{_unitdir}/
install -m 644 -p %{SOURCE2} %{buildroot}%{_unitdir}/
install -m 644 -p %{SOURCE3} %{buildroot}%{_unitdir}/
rm -rf %{buildroot}%{_initrddir}
%else
mkdir -p %{buildroot}/etc/rc.d/init.d
install -D -m755 etc/init.d.slurm    %{buildroot}/etc/rc.d/init.d/slurm
install -D -m755 etc/init.d.slurmdbd %{buildroot}/etc/rc.d/init.d/slurmdbd
%endif
install -D -m644 etc/slurm.conf.example %{buildroot}%{_sysconfdir}/slurm.conf.example
install -D -m644 etc/cgroup.conf.example %{buildroot}%{_sysconfdir}/cgroup.conf.example
install -D -m644 etc/cgroup_allowed_devices_file.conf.example %{buildroot}%{_sysconfdir}/cgroup_allowed_devices_file.conf.example
install -D -m755 etc/cgroup.release_common.example %{buildroot}%{_sysconfdir}/cgroup.release_common.example
install -D -m755 etc/cgroup.release_common.example %{buildroot}%{_sysconfdir}/cgroup/release_freezer
install -D -m755 etc/cgroup.release_common.example %{buildroot}%{_sysconfdir}/cgroup/release_cpuset
install -D -m755 etc/cgroup.release_common.example %{buildroot}%{_sysconfdir}/cgroup/release_memory
install -D -m644 etc/slurmdbd.conf.example %{buildroot}%{_sysconfdir}/slurmdbd.conf.example
install -D -m755 etc/slurm.epilog.clean %{buildroot}%{_sysconfdir}/slurm.epilog.clean
install -D -m755 contribs/sgather/sgather %{buildroot}%{_bindir}/sgather
install -D -m755 contribs/sjstat %{buildroot}%{_bindir}/sjstat

rm -f %{buildroot}/%{_mandir}/man1/sjobexitmod.1
%{buildroot}%{_bindir}/sjobexitmod --roff > %{buildroot}/%{_mandir}/man1/sjobexitmod.1
rm -f %{buildroot}/%{_mandir}/man1/sjstat.1
%{buildroot}%{_bindir}/sjstat --roff > %{buildroot}/%{_mandir}/man1/sjstat.1

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo '%{_libdir}/slurm' > %{buildroot}/etc/ld.so.conf.d/slurm.conf
chmod 644 %{buildroot}/etc/ld.so.conf.d/slurm.conf

# Make pkg-config file
mkdir -p %{buildroot}/%{_libdir}/pkgconfig
cat >%{buildroot}/%{_libdir}/pkgconfig/slurm.pc <<EOF
includedir=%{_prefix}/include
libdir=%{_libdir}

Cflags: -I\${includedir}
Libs: -L\${libdir} -lslurm
Description: Slurm API
Name: %{name}
Version: %{version}
EOF

find %{buildroot} -name '*.la' | xargs rm -f

# this is upstream to remove bluegene support
rm -f %{buildroot}/%{_libdir}/slurm/job_submit_cnode.so
rm -f %{buildroot}/%{_libdir}/slurm/select_bluegene.so
rm -f %{buildroot}/%{_libdir}/slurm/libsched_if.so
rm -f %{buildroot}/%{_libdir}/slurm/libsched_if64.so
rm -f %{buildroot}/%{_libdir}/slurm/runjob_plugin.so
rm -f %{buildroot}/%{_mandir}/man5/bluegene*
rm -f %{buildroot}/%{_sbindir}/sfree
rm -f %{buildroot}/%{_sbindir}/slurm_epilog
rm -f %{buildroot}/%{_sbindir}/slurm_prolog

# not sure why these get removed
rm -f %{buildroot}/%{_libdir}/slurm/job_submit_defaults.so
rm -f %{buildroot}/%{_libdir}/slurm/job_submit_logging.so
rm -f %{buildroot}/%{_libdir}/slurm/job_submit_partition.so

# fix perllocal.pod
rm -f %{buildroot}/%{_libdir}/perl5/perllocal.pod

%post
/sbin/ldconfig
%if 0%{?fedora} > 15
%if 0%{?fedora} > 17
%systemd_post slurmd.service
%systemd_post slurmctld.service
%else
if [ $1 -eq 1 ] ; then
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%endif
%else # EPEL thing
if [ $1 -eq 1 ] ; then
    # Initial installation 
    /sbin/chkconfig --add slurmd
fi
%endif

%post slurmdbd
%if 0%{?fedora} > 15
%if 0%{?fedora} > 17
%systemd_post slurmdbdd.service
%else
if [ $1 -eq 1 ] ; then
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%endif
%else # EPEL thing
if [ $1 -eq 1 ] ; then
    # Initial installation 
    /sbin/chkconfig --add slurmdbd
fi
%endif

%preun
%if 0%{?fedora} > 15
%if 0%{?fedora} > 17
%systemd_preun slurmd.service
%systemd_preun slurmctld.service
%else
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable slurmd.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable slurmctld.service > /dev/null 2>&1 || :
    /bin/systemctl stop slurmd.service > /dev/null 2>&1 || :
    /bin/systemctl stop slurmctld.service > /dev/null 2>&1 || :
fi
%endif
%else # EPEL thing
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /sbin/service slurm stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del slurm >/dev/null 2>&1 || :
fi
%endif

%preun slurmdbd
%if 0%{?fedora} > 15
%if 0%{?fedora} > 17
%systemd_preun slurmdbd.service
%else
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable slurmdbd.service > /dev/null 2>&1 || :
    /bin/systemctl stop slurmdbd.service > /dev/null 2>&1 || :
fi
%endif
%else # EPEL thing
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /sbin/service slurmdbd stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del slurmdbd >/dev/null 2>&1 || :
fi
%endif

%postun
/sbin/ldconfig
%if 0%{?fedora} > 15
%if 0%{?fedora} > 17
%systemd_postun_with_restart slurmd.service
%systemd_postun_with_restart slurmctld.service
%else
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart slurmd.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart slurmctld.service >/dev/null 2>&1 || :
fi
%endif
%else #EPEL thing
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /sbin/service slurm condrestart
fi
%endif

%postun slurmdbd
%if 0%{?fedora} > 15
%if 0%{?fedora} > 17
%systemd_postun_with_restart slurmdbd.service
%else
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart slurmdbd.service >/dev/null 2>&1 || :
fi
%endif
%else #EPEL thing
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /sbin/service slurmdbd condrestart
fi
%endif

%define slurmdocs BUILD.NOTES COPYING DISCLAIMER INSTALL LICENSE.OpenSSL META NEWS README.rst RELEASE_NOTES 

%files
%defattr(-,root,root,0755)
%doc %{slurmdocs}
%doc %{_docdir}/%{name}-%{version}
/etc/ld.so.conf.d/slurm.conf
%if 0%{?fedora} > 15
%{_unitdir}/slurmd.service
%{_unitdir}/slurmctld.service
%else
/etc/rc.d/init.d/slurm
%endif
%{_bindir}/s*
%exclude %{_bindir}/sjobexitmod
%exclude %{_bindir}/sjstat
%{_sbindir}/slurmctld
%{_sbindir}/slurmd
%{_sbindir}/slurmstepd
%{_libdir}/*.so.*
%{_libdir}/slurm/src/*
%{_mandir}/man1/*
%{_mandir}/man5/acct_gather.*
%{_mandir}/man5/ext_sensors.*
%{_mandir}/man5/cgroup.*
%{_mandir}/man5/cray.*
%{_mandir}/man5/gres.*
%{_mandir}/man5/nonstop.*
%{_mandir}/man5/slurm.*
%{_mandir}/man5/topology.*
%{_mandir}/man5/wiki.*
%{_mandir}/man8/slurmctld.*
%{_mandir}/man8/slurmd.*
%{_mandir}/man8/slurmstepd*
%{_mandir}/man8/spank*
%config (noreplace) %{_sysconfdir}/slurm.conf.example
%config (noreplace) %{_sysconfdir}/cgroup.conf.example
%config (noreplace) %{_sysconfdir}/cgroup_allowed_devices_file.conf.example
%config (noreplace) %{_sysconfdir}/cgroup.release_common.example
%config (noreplace) %{_sysconfdir}/cgroup/release_freezer
%config (noreplace) %{_sysconfdir}/cgroup/release_cpuset
%config (noreplace) %{_sysconfdir}/cgroup/release_memory
%config (noreplace) %{_sysconfdir}/slurm.epilog.clean
%exclude %{_mandir}/man1/sjobexit*
%exclude %{_mandir}/man1/sjstat*

%files devel
%defattr(-,root,root,0755)
%doc %{slurmdocs}
%dir %attr(0755,root,root)
%dir %{_prefix}/include/slurm
%{_prefix}/include/slurm/*
%{_mandir}/man3/slurm_*
%dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/slurm.pc
%{_libdir}/*.so

%files auth-none
%defattr(-,root,root)
%doc %{slurmdocs}
%{_libdir}/slurm/auth_none.so

%files munge
%defattr(-,root,root,0755)
%doc %{slurmdocs}
%{_libdir}/slurm/auth_munge.so
%{_libdir}/slurm/crypto_munge.so


%files pam_slurm
%defattr(-,root,root,0755)
%doc %{slurmdocs}
/%{_lib}/security/pam_slurm.so

%files perlapi
%defattr(-,root,root,0755)
%doc %{slurmdocs}
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto/
%{_mandir}/man3/*.3pm.*

%files plugins
%defattr(-,root,root,0755)
%doc %{slurmdocs}
%dir %{_libdir}/slurm
%{_libdir}/slurm/accounting_storage_filetxt.so
%{_libdir}/slurm/accounting_storage_none.so
%{_libdir}/slurm/accounting_storage_slurmdbd.so
%{_libdir}/slurm/acct_gather_filesystem_lustre.so
%{_libdir}/slurm/acct_gather_filesystem_none.so
%{_libdir}/slurm/acct_gather_infiniband_none.so
%{_libdir}/slurm/acct_gather_energy_none.so
%{_libdir}/slurm/acct_gather_energy_ipmi.so
%{_libdir}/slurm/acct_gather_energy_rapl.so
%{_libdir}/slurm/acct_gather_profile_none.so
%{_libdir}/slurm/acct_gather_profile_hdf5.so
%{_libdir}/slurm/checkpoint_none.so
%{_libdir}/slurm/checkpoint_ompi.so
%{_libdir}/slurm/core_spec_cray.so
%{_libdir}/slurm/core_spec_none.so
%{_libdir}/slurm/crypto_openssl.so
%{_libdir}/slurm/ext_sensors_none.so
%{_libdir}/slurm/ext_sensors_rrd.so
%{_libdir}/slurm/gres_gpu.so
%{_libdir}/slurm/gres_mic.so
%{_libdir}/slurm/gres_nic.so
%{_libdir}/slurm/job_container_cncu.so
%{_libdir}/slurm/job_container_none.so
%{_libdir}/slurm/job_submit_all_partitions.so
%{_libdir}/slurm/job_submit_cray.so
%{_libdir}/slurm/job_submit_require_timelimit.so
%{_libdir}/slurm/job_submit_throttle.so
%{_libdir}/slurm/jobacct_gather_aix.so
%{_libdir}/slurm/jobacct_gather_cgroup.so
%{_libdir}/slurm/jobacct_gather_linux.so
%{_libdir}/slurm/jobacct_gather_none.so
%{_libdir}/slurm/jobcomp_filetxt.so
%{_libdir}/slurm/jobcomp_none.so
%{_libdir}/slurm/jobcomp_script.so
%{_libdir}/slurm/mpi_lam.so
%{_libdir}/slurm/mpi_mpich1_p4.so
%{_libdir}/slurm/mpi_mpich1_shmem.so
%{_libdir}/slurm/mpi_mpichgm.so
%{_libdir}/slurm/mpi_mpichmx.so
%{_libdir}/slurm/mpi_mvapich.so
%{_libdir}/slurm/mpi_openmpi.so
%{_libdir}/slurm/mpi_pmi2.so
%{_libdir}/slurm/mpi_none.so
%{_libdir}/slurm/preempt_none.so
%{_libdir}/slurm/preempt_partition_prio.so
%{_libdir}/slurm/preempt_qos.so
%{_libdir}/slurm/priority_basic.so
%{_libdir}/slurm/priority_multifactor.so
%{_libdir}/slurm/proctrack_cgroup.so
%{_libdir}/slurm/proctrack_linuxproc.so
%{_libdir}/slurm/proctrack_pgid.so
%{_libdir}/slurm/launch_slurm.so
%{_libdir}/slurm/sched_backfill.so
%{_libdir}/slurm/sched_builtin.so
%{_libdir}/slurm/sched_hold.so
%{_libdir}/slurm/sched_wiki.so
%{_libdir}/slurm/sched_wiki2.so
%{_libdir}/slurm/select_alps.so
%{_libdir}/slurm/select_cray.so
%{_libdir}/slurm/select_cons_res.so
%{_libdir}/slurm/select_linear.so
%{_libdir}/slurm/select_serial.so
%{_libdir}/slurm/slurmctld_nonstop.so
%{_libdir}/slurm/switch_generic.so
%{_libdir}/slurm/switch_none.so
%{_libdir}/slurm/switch_cray.so
%{_libdir}/slurm/task_none.so
%{_libdir}/slurm/task_affinity.so
%{_libdir}/slurm/task_cgroup.so
%{_libdir}/slurm/task_cray.so
%{_libdir}/slurm/topology_3d_torus.so
%{_libdir}/slurm/topology_node_rank.so
%{_libdir}/slurm/topology_none.so
%{_libdir}/slurm/topology_tree.so

%files sjobexit
%defattr(-,root,root,0755)
%doc %{slurmdocs}
%{_bindir}/sjobexitmod
%{_mandir}/man1/sjobexit*

%files sjstat
%defattr(-,root,root,0755)
%doc %{slurmdocs}
%{_bindir}/sjstat
%{_mandir}/man1/sjstat*

%files slurmdbd
%defattr(-,root,root,0755)
%doc %{slurmdocs}
%if 0%{?fedora} > 15
%{_unitdir}/slurmdbd.service
%else
/etc/rc.d/init.d/slurmdbd
%endif
%{_sbindir}/slurmdbd
%{_mandir}/man5/slurmdbd.*
%{_mandir}/man8/slurmdbd.*
%config %{_sysconfdir}/slurmdbd.conf.example

%files slurmdb-direct
%defattr(-,root,root,0755)
%doc %{slurmdocs}
%config (noreplace) %{perl_vendorarch}/config.slurmdb.pl
%{_sbindir}/moab_2_slurmdb

%files sql
%defattr(-,root,root,0755)
%doc %{slurmdocs}
%{_libdir}/slurm/accounting_storage_mysql.so
%{_libdir}/slurm/jobcomp_mysql.so

%files torque
%defattr(-,root,root,0755)
%doc %{slurmdocs}
%{_bindir}/pbsnodes
%{_bindir}/qalter
%{_bindir}/qdel
%{_bindir}/qhold
%{_bindir}/qrerun
%{_bindir}/qrls
%{_bindir}/qstat
%{_bindir}/qsub
%{_bindir}/mpiexec
%{_bindir}/generate_pbs_nodefile
%{_libdir}/slurm/job_submit_pbs.so
%{_libdir}/slurm/spank_pbs.so

%files lua
%defattr(-,root,root,0755)
%doc contribs/lua/proctrack.lua %{slurmdocs}
%{_libdir}/slurm/job_submit_lua.so
%{_libdir}/slurm/proctrack_lua.so

%changelog
* Fri Oct 3 2014 David Brown <david.brown@pnnl.gov> - 14.03.8-1
- Initial build of slurm
