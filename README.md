# Python module for BigV

This is an initial attempt at a Python module for BigV, with the eventual idea 
that this will be incorporated into an Ansible module.

*Note* This is a wrapper around the BigV [command-line tool][1], rather than a tool
which consumes the REST API. The REST API is not yet final/fully public,
although it is documented (unoficially) [here][2]

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

[1]: http://www.bigv.io/download
[2]: http://bigv-api-docs.ichilton.co.uk/api/
