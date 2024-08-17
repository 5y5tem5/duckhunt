import dns.resolver
import socket
import argparse
import sys
import whois
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--domain', type=str, help='domain')
def get_soa_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'SOA')
        soa_record = answers[0]
        primary_ns = soa_record.mname.to_text()
        return primary_ns, soa_record
    except Exception as e:
        return None, str(e)

def check_authoritative_response(domain, primary_ns):
    try:
        resolver = dns.resolver.Resolver()
        ns_ip=socket.gethostbyname(primary_ns.rstrip('.'))
        resolver.nameservers = [ns_ip]
        answers = resolver.resolve(domain, 'SOA')
        is_authoritative = bool(answers.response.flags & dns.flags.AA)
        return is_authoritative
    except Exception as e:
        return str(e)

def get_whoisdata(domain):
    try:
        domain_info = whois.query(domain)
        nameservers = domain_info.name_servers
        return nameservers
    except Exception as e:
        return f"Error: {str(e)}"

args = parser.parse_args()

if args.domain is None:
    print(f"domain not set: duckhunt.py -d example.com")
    sys.exit(-1)

domain = args.domain
primary_ns, soa_record = get_soa_record(domain)

if primary_ns:
    is_authoritative = check_authoritative_response(domain, primary_ns)
    print(f"Domain:{domain}; Primary:{primary_ns}; AA: {is_authoritative}")
else:
    is_authoritative =False


if not is_authoritative:
    whois_nameservers = get_whoisdata(domain)
    print(f"Domain:{domain}; Whois NSes: {whois_nameservers}")
