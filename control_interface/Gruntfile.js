'use strict';

// # Globbing
// for performance reasons we're only matching one level down:
// 'test/spec/{,*/}*.js'
// use this if you want to recursively match all subfolders:
// 'test/spec/**/*.js'

module.exports = function (grunt) {
    // load all grunt tasks
    require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

    grunt.initConfig({
        watch: {
            options: {
                nospawn: true
            },
            coffee: {
                files: 'coffee/{,*/}*.coffee',
                tasks: ['coffee'],
            },
            handlebars: {
                files: ['templates/{,*/}*.hbs'],
                tasks: ['handlebars']
            },
            sass: {
                files: ['sass/{,*/}*.scss'],
                tasks: ['sass']
            },
        },
        coffee: {
            compile: {
                expand: true,
                cwd: 'coffee/',
                src: ['{,*/}*.coffee'],
                dest: 'js/',
                ext: '.js'
            }
        },
        handlebars: {
            options: {
                namespace: 'com.firsteast.templates',
                processName: function(filePath) {
                    return filePath.replace(/templates\//, '').replace(/\.hbs$/, '');
                }
            },
            all: {
                files: {
                    "js/templates.js": ["templates{,*/}*.hbs"]
                }
            }
        },
        sass: {
            all: {
                files: {
                    'css/main.css': 'sass/main.scss'
                }
            }
        }
    });
};
