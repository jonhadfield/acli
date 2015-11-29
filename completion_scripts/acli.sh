
_acli()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 1 ]; then
        COMPREPLY=( $( compgen -fW '--version -h --help --install-completion --region= --access_key_id= --secret_access_key= ami eip account lc elb secgroup s3 asg ec2 vpc clean route53 es' -- $cur) )
    else
        case ${COMP_WORDS[1]} in
            ami)
            _acli_ami
        ;;
            eip)
            _acli_eip
        ;;
            account)
            _acli_account
        ;;
            lc)
            _acli_lc
        ;;
            elb)
            _acli_elb
        ;;
            secgroup)
            _acli_secgroup
        ;;
            s3)
            _acli_s3
        ;;
            asg)
            _acli_asg
        ;;
            ec2)
            _acli_ec2
        ;;
            vpc)
            _acli_vpc
        ;;
            clean)
            _acli_clean
        ;;
            route53)
            _acli_route53
        ;;
            es)
            _acli_es
        ;;
        esac

    fi
}

_acli_ami()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -W ' info list ls' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            info)
            _acli_ami_info
        ;;
            list)
            _acli_ami_list
        ;;
            ls)
            _acli_ami_ls
        ;;
        esac

    fi
}

_acli_ami_info()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -fW ' ' -- $cur) )
    fi
}

_acli_ami_list()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_ami_ls()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_eip()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -W ' info list ls' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            info)
            _acli_eip_info
        ;;
            list)
            _acli_eip_list
        ;;
            ls)
            _acli_eip_ls
        ;;
        esac

    fi
}

_acli_eip_info()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -fW ' ' -- $cur) )
    fi
}

_acli_eip_list()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_eip_ls()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_account()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 2 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_lc()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -W ' list ls' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            list)
            _acli_lc_list
        ;;
            ls)
            _acli_lc_ls
        ;;
        esac

    fi
}

_acli_lc_list()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_lc_ls()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_elb()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -W ' info list ls' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            info)
            _acli_elb_info
        ;;
            list)
            _acli_elb_list
        ;;
            ls)
            _acli_elb_ls
        ;;
        esac

    fi
}

_acli_elb_info()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -fW ' ' -- $cur) )
    fi
}

_acli_elb_list()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_elb_ls()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_secgroup()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -W ' info list ls' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            info)
            _acli_secgroup_info
        ;;
            list)
            _acli_secgroup_list
        ;;
            ls)
            _acli_secgroup_ls
        ;;
        esac

    fi
}

_acli_secgroup_info()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -fW ' ' -- $cur) )
    fi
}

_acli_secgroup_list()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_secgroup_ls()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_s3()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -fW ' info list del ls rm cp' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            info)
            _acli_s3_info
        ;;
            list)
            _acli_s3_list
        ;;
            del)
            _acli_s3_del
        ;;
            ls)
            _acli_s3_ls
        ;;
            rm)
            _acli_s3_rm
        ;;
            cp)
            _acli_s3_cp
        ;;
        esac

    fi
}

_acli_s3_info()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -fW ' ' -- $cur) )
    fi
}

_acli_s3_list()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_s3_del()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_s3_ls()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_s3_rm()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_s3_cp()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -fW ' ' -- $cur) )
    fi
}

_acli_asg()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -fW ' info mem list ls net cpu delete' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            info)
            _acli_asg_info
        ;;
            mem)
            _acli_asg_mem
        ;;
            list)
            _acli_asg_list
        ;;
            ls)
            _acli_asg_ls
        ;;
            net)
            _acli_asg_net
        ;;
            cpu)
            _acli_asg_cpu
        ;;
            delete)
            _acli_asg_delete
        ;;
        esac

    fi
}

_acli_asg_info()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_asg_mem()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_asg_list()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_asg_ls()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_asg_net()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_asg_cpu()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_asg_delete()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_ec2()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -fW ' info list stop reboot terminate summary start ls vols net cpu' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            info)
            _acli_ec2_info
        ;;
            list)
            _acli_ec2_list
        ;;
            stop)
            _acli_ec2_stop
        ;;
            reboot)
            _acli_ec2_reboot
        ;;
            terminate)
            _acli_ec2_terminate
        ;;
            summary)
            _acli_ec2_summary
        ;;
            start)
            _acli_ec2_start
        ;;
            ls)
            _acli_ec2_ls
        ;;
            vols)
            _acli_ec2_vols
        ;;
            net)
            _acli_ec2_net
        ;;
            cpu)
            _acli_ec2_cpu
        ;;
        esac

    fi
}

_acli_ec2_info()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_ec2_list()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_ec2_stop()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_ec2_reboot()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_ec2_terminate()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_ec2_summary()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_ec2_start()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_ec2_ls()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_ec2_vols()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_ec2_net()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_ec2_cpu()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_vpc()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -W ' info list ls' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            info)
            _acli_vpc_info
        ;;
            list)
            _acli_vpc_list
        ;;
            ls)
            _acli_vpc_ls
        ;;
        esac

    fi
}

_acli_vpc_info()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -fW ' ' -- $cur) )
    fi
}

_acli_vpc_list()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_vpc_ls()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_clean()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -W ' delete_orphaned_snapshots delete_unnammed_volumes' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            delete_orphaned_snapshots)
            _acli_clean_delete_orphaned_snapshots
        ;;
            delete_unnammed_volumes)
            _acli_clean_delete_unnammed_volumes
        ;;
        esac

    fi
}

_acli_clean_delete_orphaned_snapshots()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_clean_delete_unnammed_volumes()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_route53()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -W ' info list ls' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            info)
            _acli_route53_info
        ;;
            list)
            _acli_route53_list
        ;;
            ls)
            _acli_route53_ls
        ;;
        esac

    fi
}

_acli_route53_info()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -fW ' ' -- $cur) )
    fi
}

_acli_route53_list()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_route53_ls()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_es()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -W ' info list ls' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            info)
            _acli_es_info
        ;;
            list)
            _acli_es_list
        ;;
            ls)
            _acli_es_ls
        ;;
        esac

    fi
}

_acli_es_info()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -fW ' ' -- $cur) )
    fi
}

_acli_es_list()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

_acli_es_ls()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -W ' ' -- $cur) )
    fi
}

complete -F _acli acli