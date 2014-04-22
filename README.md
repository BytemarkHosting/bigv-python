# Python module for BigV

This is an initial attempt at a Python module for BigV, with the eventual idea
that this will be incorporated into an Ansible module.

*Note* This is a wrapper around the BigV [command-line tool][1], rather than a
tool which consumes the REST API. The REST API is documented [here][2] (and its
docs are on Github [here][3]).

## TODO

* Testing
* Packaging
* Everything else

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
[2]: http://bigv-api-docs.ichilton.co.uk/api/
[3]: https://github.com/ichilton/bytemark-bigv-api-doc

<!--- vim:textwidth=80 
--->


