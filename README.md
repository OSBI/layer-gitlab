# Overview

This charm provides Pentaho Data Integration 6 for Extract, Transform
and Load operations flexibly on a single server.

Pentaho Data Integration[http://pentaho.com] is an graphical ETL tool
that can be used for building data flows and manipulation. Once the ETL
has be written it can then be deployed and run on a higher powered server.

This charm provides actions that allow for running of a Job or Transformation
directly on the server. It also provides the Carte webservice that allows
users to run ETL code on the remote server from within the PDI GUI.

To mataintain flexibility, this charm requires a Java charm to be 
related to it, so administrators can pick their favourite "flavour"
of Java.

# Usage

To deploy this PDI charm you run:

    juju deploy cs:~f-tom-n/trusty/pentahodataintegration pdi
    juju deploy cs:~kwmonroe/trusty/openjdk java
    juju deploy add-relation java pdi

Deploying the PDI charm will create a server and install PDI, but it is not
executable until you have deployed a Java charm and added the relation that
will install Java on the container. This enables users to select an
alternative JVM without having to make changes to the PDI charm or tear down
the server.

If you are planning on using Carte, make sure you expose the Carte port
(9999) by default:

    juju expose pdi

To deploy a different version of PDI or download from a different mirror you 
can update the pdi_url config value to point to a different PDI zip archive:
    
    juju set pdi pdi_url='http://.....' 

To change the port carte runs on, you can change the carte port:

     juju set pdi carte_port='9999'

To override the default PDI JAVA_OPTS(memory limits etc) you can set an
alternative value buy running:

     juju set pdi java_opts='-Xmx=4G'

To set an alternative Carte password, enter the unencypted version by 
running:

    juju set pdi carte_password='my_new_password'

# Limitations

This charm does not currently have any config options, nor does it scale.
This may change if other relations are added that would benefit from such
functionality.


# Contact Information

- <kevin.monroe@canonical.com>
