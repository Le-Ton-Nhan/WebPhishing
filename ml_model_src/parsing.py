
from .urlIocs import IoCIdentifier
from typing import Tuple


def ioc_protection(text: str) -> IoCIdentifier:
    iid = IoCIdentifier(text)
    iid.ioc_identify()
    return iid.ioc_list

def report_parsing(text: str):
    iid = ioc_protection(text)
    return iid
    # return iid, doc

# report_text = "Benign activity ran for most of the morning while the tools were being setup for the day.  The activity was modified so the hosts would open Firefox and browse to http://215.237.119.171/config.html.  The simulated host then entered URL for BITS Micro APT as http://68.149.51.179/ctfhost2.exe.   We used the exploited Firefox backdoor to initiate download of ctfhost2.exe via the Background Intelligent Transfer Service (BITS).  Our server indicated the file was successfully downloaded using the BITS protocol, and soon after Micro APT was executed on the target and connected out to 113.165.213.253:80 for C2.  The attacker tried to elevate using a few different drivers, but it failed once again due to the computer having been restarted without disabling driver signature enforcement.  BBN tried using BCDedit to permanently disable driver signing, but it did not seem to work during the engagement as the drivers failed to work unless driver signing was explicitly disabled during boot."
# cti_doc = report_parsing(report_text)
# print(cti_doc)