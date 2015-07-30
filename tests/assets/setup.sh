#!/bin/bash

echo '####### Shallow-cloning Repositories'
if [ ! -d repos ]; then
    mkdir repos
    cd repos

    echo '  Java'
    git clone --depth 1 https://github.com/Netflix/SimianArmy.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/apache/maven.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/PhilJay/MPAndroidChart.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/apache/cassandra.git 1> /dev/null 2> /dev/null

    echo '  JavaScript'
    git clone --depth 1 https://github.com/visionmedia/superagent.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/jquery/qunit.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/gruntjs/grunt.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/airbnb/javascript.git 1> /dev/null 2> /dev/null

    echo '  Objective-C'
    git clone --depth 1 https://github.com/laiso/WebScraper-iOS 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/sparkle-project/Sparkle.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/CoderMJLee/MJExtension.git 1> /dev/null 2> /dev/null

    git clone --depth 1 https://github.com/zachwarren/UITableViewController-Challenge-Solution.git 1> /dev/null 2> /dev/null

    echo '  PHP'
    git clone --depth 1 https://github.com/composer/composer.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/laravel/laravel.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/justinwalsh/daux.io.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/marmelab/microrest.php.git 1> /dev/null 2> /dev/null

    echo '  Python'
    git clone --depth 1 https://github.com/ansible/ansible.git 1> /dev/null 2> /dev/null 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/maraujop/django-crispy-forms.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/opsschool/curriculum.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/mozilla/webpay.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/mapbox/mbutil.git 1> /dev/null 2> /dev/null

    echo '  Ruby'
    git clone --depth 1 https://github.com/andymeneely/squib.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/schacon/ruby-git.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/nomad/shenzhen.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/github/janky.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/github/linguist.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/libgit2/docurium.git 1> /dev/null 2> /dev/null

    echo '  C#'
    git clone --depth 1 https://github.com/ApocalypticOctopus/Epic.Numbers.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/chocolatey/choco.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/ShareX/ShareX.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/aspnet/WebSockets.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/aws/aws-sdk-net.git 1> /dev/null 2> /dev/null

    echo '  C++'
    git clone --depth 1 https://github.com/SFTtech/openage.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/drmeister/externals-clasp.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/atom/electron.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/Microsoft/IEDiagnosticsAdapter.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/google/angle.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/mapbox/variant.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/google/primarysources.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/apache/mesos.git 1> /dev/null 2> /dev/null

    echo '  C'
    git clone --depth 1 https://github.com/Distrotech/gnome-vfs.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/drobin/grs.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/lpereira/lwan.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/joyent/http-parser.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/h2o/h2o.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/libgit2/libgit2.git 1> /dev/null 2> /dev/null

else
    echo '  Previous clones are still around. Exiting.'
fi
