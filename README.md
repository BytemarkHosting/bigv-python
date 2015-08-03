# Python module for BigV
<img align='right' style='float: left' src='https://www.bigv.io/images/bigv_logo.png'/>

This is an initial attempt at a Python module for BigV, with the eventual idea
that this will be incorporated into an Ansible module.

This tool consumes the BigV REST API. The REST API is documented [here][2] (and
its docs are on Github [here][3]), and depends on the python-requests [module][4].

## Examples

    import bigv
  
    act = bigv.BigVAccount(username="alice",password="testing",account="mystuff")
    for m in act.machines():
      print "Machine has %d discs" % len(list(m.discs()))
      print m.info()

## Usage with Ansible

This repository now contains (possibly buggy) implementations of two Ansible
modules, `bigv-disc` and `bigv-vm` which are capable of creating new machines
and discs. Both modules are idempotent, but note that they will only ever
*create* and *delete* discs and VMs, and will never *edit* them.

Spec changes will need to be done manually.

A sample [playbook](sample-playbook.yml) is provided which shows basic usage of
the two modules.

[1]: http://www.bigv.io/download
[2]: http://www.bigv.io/support/api/
[3]: https://github.com/ichilton/bytemark-bigv-api-doc
[4]: http://docs.python-requests.org/en/latest/

## Manual Installation Instructions

Since this is very much still in development, installation is a fairly manual process which allows you to pull changes from the git repo directly:

1. Checkout the repo somewhere
2. Install the Python module dependencies ('$ pip install -r requirements.txt')
3. Create a symlink to the `bigv/` directory somewhere in the Python Path, you can check it works by running `python -c 'import bigv'` and making sure it returns 0
4. Create a `library/` directory in the same directory as your Ansible playbook, symlink `bigv-disc` and `bigv-vm` into it.

<!--- vim:textwidth=80 
--->


