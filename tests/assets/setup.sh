#!/bin/bash

echo '####### Shallow-cloning Repositories'
if [ ! -d repos ]; then
    mkdir repos
    cd repos

    echo '  Java'
    git clone --depth 1 https://github.com/Netflix/SimianArmy.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/apache/maven.git 1> /dev/null 2> /dev/null

    echo '  JavaScript'
    git clone --depth 1 https://github.com/visionmedia/superagent.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/jquery/qunit.git 1> /dev/null 2> /dev/null

    echo '  Objective-C'
    git clone --depth 1 https://github.com/laiso/WebScraper-iOS 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/sparkle-project/Sparkle.git 1> /dev/null 2> /dev/null

    echo '  PHP'
    git clone --depth 1 https://github.com/composer/composer.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/laravel/laravel.git 1> /dev/null 2> /dev/null

    echo '  Python'
    git clone --depth 1 https://github.com/ansible/ansible.git 1> /dev/null 2> /dev/null 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/maraujop/django-crispy-forms.git 1> /dev/null 2> /dev/null

    echo '  Ruby'
    git clone --depth 1 https://github.com/andymeneely/squib.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/schacon/ruby-git.git 1> /dev/null 2> /dev/null

    echo '  C#'
    git clone --depth 1 https://github.com/ApocalypticOctopus/Epic.Numbers.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/chocolatey/choco.git 1> /dev/null 2> /dev/null

    echo '  C++'
    git clone --depth 1 https://github.com/SFTtech/openage.git 1> /dev/null 2> /dev/null
    git clone --depth 1 https://github.com/drmeister/externals-clasp.git 1> /dev/null 2> /dev/null
else
    echo '  Previous clones are still around. Exiting.'
fi