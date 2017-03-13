# HashHound
Python Module for automating White-Listing and (soon-to-be) Black-Listing

The idea and/or intent of this tool is that users can:

1) Add flexibility and interoperability with whitelisting tools.  Tools like Kansa or any other tool that generates hashes to either validate those hashes (md5/sha1) in their environment based of off a whitelist source such as the NSRL's RDS  Hashsets.

2) Develop their own hashset from a TRUSTED image source. 
Note: A TRUSTED image would be an image build either not yet deployed on a network due to the possibility that it could be compromised. Or, an image you're confident hasn't been tampered with.  To state the obvious, if you white list a compromised image, you're essentially saying bad files are good.
    
3) Combine an outside hash dataset with their own (combining options 1 and 2)

4) Be modular; this script can be ran as a server, ran as an imported module or ran locally.

5) Interoperate with the nsrllookup client.
