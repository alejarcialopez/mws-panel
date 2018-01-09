# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-04 17:07
from __future__ import unicode_literals

from django.db import migrations, models


php_lib_values = [
    ('libawl-php', 'Andrew''s Web Libraries - PHP Utility Libraries'),
    ('libarc-php', 'Flexible RDF system for semantic web and PHP practitioners'),
    ('libfpdf-tpl-php', 'PHP library to use PDF templates with FPDF'),
    ('libfpdi-php', 'PHP library for importing existing PDF documents into FPDF'),
    ('libgraphite-php', 'PHP Linked Data Library'),
    ('libgv-php5', 'PHP5 bindings for graphviz'),
    ('libkohana2-modules-php', 'lightweight PHP5 MVC framework (extension modules)'),
    ('libkohana2-php', 'lightweight PHP5 MVC framework'),
    ('libmarkdown-php', 'PHP library for rendering Markdown data'),
    ('libnusoap-php', 'SOAP toolkit for PHP'),
    ('liboauth-php', 'PHP library implementing the OAuth secure authentication protocol'),
    ('libow-php5', '"Dallas 1-wire support: PHP5 bindings"'),
    ('libownet-php', '"Dallas 1-wire support: PHP OWNet library"'),
    ('libpuzzle-php', 'quick similar image finder - PHP bindings'),
    ('libsparkline-php', 'sparkline graphing library for php'),
    ('php5-adodb', 'Extension optimising the ADOdb database abstraction library'),
    ('php5-apcu', 'APC User Cache for PHP 5'),
    ('php5-cgi', 'server-side, HTML-embedded scripting language (CGI binary)'),
    ('php5-dbg', 'Debug symbols for PHP5'),
    ('php5-dev', 'Files for PHP5 module development'),
    ('php5-enchant', 'Enchant module for php5'),
    ('php5-exactimage', 'fast image manipulation library (PHP bindings)'),
    ('php5-fpm', 'server-side HTML-embedded scripting language (FPM-CGI binary)'),
    ('php5-gdcm', 'Grassroots DICOM PHP5 bindings'),
    ('php5-gearman', 'PHP wrapper to libgearman'),
    ('php5-geoip', 'GeoIP module for php5'),
    ('php5-geos', 'GEOS bindings for PHP'),
    ('php5-gmp', 'GMP module for php5'),
    ('php5-gnupg', 'wrapper around the gpgme library'),
    ('php5-igbinary', 'igbinary extension'),
    ('php5-imagick', 'Provides a wrapper to the ImageMagick library'),
    ('php5-imap', 'IMAP module for php5'),
    ('php5-interbase', 'interbase/firebird module for php5'),
    ('php5-intl', 'internationalisation module for php5'),
    ('php5-lasso', 'Library for Liberty Alliance and SAML protocols - PHP 5 bindings'),
    ('php5-librdf', 'PHP5 language bindings for the Redland RDF library'),
    ('php5-libvirt-php', 'libvirt bindings for PHP'),
    ('php5-mapscript', 'php5-cgi module for MapServer'),
    ('php5-mcrypt', 'MCrypt module for php5'),
    ('php5-memcache', 'memcache extension module for PHP5'),
    ('php5-memcached', 'memcached extension module for PHP5, uses libmemcached'),
    ('php5-mongo', 'MongoDB database driver'),
    ('php5-msgpack', 'PHP extension for interfacing with MessagePack'),
    ('php5-mysqlnd-ms', 'MySQL replication and load balancing module for PHP'),
    ('php5-oauth', 'OAuth 1.0 consumer and provider extension'),
    ('php5-odbc', 'ODBC module for php5'),
    ('php5-pecl-http', 'pecl_http module for PHP 5 Extended HTTP Support'),
    ('php5-pecl-http-dev', 'pecl_http module for PHP 5 Extended HTTP Support development headers'),
    ('php5-pgsql', 'PostgreSQL module for php5'),
    ('php5-phpdbg', 'server-side, HTML-embedded scripting language (PHPDBG binary)'),
    ('php5-pinba', 'Pinba module for PHP 5'),
    ('php5-propro', 'propro module for PHP 5'),
    ('php5-propro-dev', 'propro module for PHP 5 development headers'),
    ('php5-pspell', 'pspell module for php5'),
    ('php5-radius', 'PECL radius module for PHP 5'),
    ('php5-raphf', 'raphf module for PHP 5'),
    ('php5-raphf-dev', 'raphf module for PHP 5 development headers'),
    ('php5-recode', 'recode module for php5'),
    ('php5-redis', 'PHP extension for interfacing with Redis'),
    ('php5-remctl', 'PECL module for Kerberos-authenticated command execution'),
    ('php5-rrd', 'PHP bindings to rrd tool system'),
    ('php5-sasl', 'Cyrus SASL Extension'),
    ('php5-snmp', 'SNMP module for php5'),
    ('php5-solr', 'solr module for PHP 5'),
    ('php5-ssh2', 'Bindings for the libssh2 library'),
    ('php5-stomp', 'Streaming Text Oriented Messaging Protocol (STOMP) client module for PHP 5'),
    ('php5-svn', 'PHP Bindings for the Subversion Revision control system'),
    ('php5-sybase', 'Sybase / MS SQL Server module for php5'),
    ('php5-tidy', 'tidy module for php5'),
    ('php5-tokyo-tyrant', 'PHP interface to Tokyo Cabinet''s network interface, Tokyo Tyrant'),
    ('php5-twig', 'Enhance performance of the Twig template engine'),
    ('php5-uprofiler', 'hierarchical profiler for PHP (extension)'),
    ('php5-vtkgdcm', 'Grassroots DICOM VTK PHP bindings'),
    ('php5-xcache', 'Fast, stable PHP opcode cacher'),
    ('php5-xdebug', 'Xdebug Module for PHP 5'),
    ('php5-xhprof', 'Hierarchical Profiler for PHP5'),
    ('php5-xmlrpc', 'XML-RPC module for php5'),
    ('php5-xsl', 'XSL module for php5'),
    ('php5-yac', 'YAC (Yet Another Cache) for PHP 5'),
    ('php5-zmq', 'ZeroMQ messaging'),
]


php_lib_mappings = [
    ('libawl-php', 'libawl-php'),
    ('libgv-php5', 'libgvc6'),
    ('libmarkdown-php', 'libmarkdown-php'),
    ('libnusoap-php', 'libnusoap-php'),
    ('libownet-php', 'libownet-php'),
    ('php5-adodb', 'libphp-adodb'),
    ('php5-dev', 'php-all-dev'),
    ('php5-sasl', 'php-auth-sasl'),
    ('php5-cgi', 'php-cgi'),
    ('php5-enchant', 'php-enchant'),
    ('php5-fpm', 'php-fpm'),
    ('php5-xsl', 'php-fxsl'),
    ('php5-gearman', 'php-gearman'),
    ('php5-geoip', 'php-geoip'),
    ('php5-gmp', 'php-gmp'),
    ('php5-gnupg', 'php-gnupg'),
    ('php5-igbinary', 'php-igbinary'),
    ('php5-imagick', 'php-imagick'),
    ('php5-imap', 'php-imap'),
    ('php5-interbase', 'php-interbase'),
    ('php5-intl', 'php-intl'),
    ('php5-libvirt-php', 'php-libvirt-php'),
    ('php5-mcrypt', 'php-mcrypt'),
    ('php5-memcache', 'php-memcache'),
    ('php5-memcached', 'php-memcached'),
    ('php5-mongo', 'php-mongodb'),
    ('php5-msgpack', 'php-msgpack'),
    ('php5-oauth', 'php-oauth'),
    ('php5-odbc', 'php-odbc'),
    ('php5-pecl-http', 'php-pecl-http'),
    ('php5-pecl-http-dev', 'php-pecl-http-dev'),
    ('php5-pgsql', 'php-pgsql'),
    ('php5-dbg', 'php-phpdbg'),
    ('php5-phpdbg', 'php-phpdbg'),
    ('php5-pinba', 'php-pinba'),
    ('php5-propro', 'php-propro'),
    ('php5-propro-dev', 'php-propro-dev'),
    ('php5-pspell', 'php-pspell'),
    ('php5-radius', 'php-radius'),
    ('php5-raphf', 'php-raphf'),
    ('php5-raphf-dev', 'php-raphf-dev'),
    ('php5-recode', 'php-recode'),
    ('php5-redis', 'php-redis'),
    ('php5-remctl', 'php-remctl'),
    ('php5-rrd', 'php-rrd'),
    ('php5-snmp', 'php-snmp'),
    ('php5-solr', 'php-solr'),
    ('php5-ssh2', 'php-ssh2'),
    ('php5-stomp', 'php-stomp'),
    ('php5-sybase', 'php-sybase'),
    ('php5-tidy', 'php-tidy'),
    ('php5-twig', 'php-twig'),
    ('php5-xdebug', 'php-xdebug'),
    ('php5-xmlrpc', 'php-xmlrpc'),
    ('php5-yac', 'php-yac'),
    ('php5-zmq', 'php-zmq'),
    ('php5-apcu', 'php5-apcu'),
]


def populate_php_lib(apps, schema_editor):
    PHPLib = apps.get_model('apimws', 'PHPLib')
    for values in php_lib_values:
        PHPLib.objects.create(name=values[0], description=values[1])


def populate_name_next_os(apps, schema_editor):
    PHPLib = apps.get_model('apimws', 'PHPLib')
    for mapping in php_lib_mappings:
        php_lib = PHPLib.objects.get(name=mapping[0])
        php_lib.name_next_os = mapping[1]
        php_lib.save()


class Migration(migrations.Migration):

    dependencies = [
        ('apimws', '0010_auto_20160506_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='phplib',
            name='name_next_os',
            field=models.CharField(blank=True, null=True, max_length=150),
        ),
        migrations.RunPython(populate_php_lib),
        migrations.RunPython(populate_name_next_os),
    ]
