module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    sass: {
      options: {
        includePaths: [
          'revolv/static/bower_components/foundation/scss',
        ]
      },
      dist: {
        options: {
          //outputStyle: 'compressed'
        },
        files: {
          'revolv/static/main.css': 'revolv/static/main.scss',
          'revolv/static/home.css': 'revolv/static/home.scss',
          'revolv/static/auth.css': 'revolv/static/auth.scss',
          'revolv/static/project.css': 'revolv/static/project.scss',
          'revolv/static/dashboard.css': 'revolv/static/dashboard.scss',
          'revolv/static/project-edit.css': 'revolv/static/project-edit.scss',
          'revolv/static/404.css': 'revolv/static/404.scss',
          'revolv/static/accounting.css': 'revolv/static/accounting.scss',
        }
      }
    },

    watch: {
      grunt: { files: ['Gruntfile.js'] },

      sass: {
        files: 'revolv/static/**/*.scss',
        tasks: ['sass']
      }
    }
  });

  grunt.loadNpmTasks('grunt-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('build', ['sass']);
  grunt.registerTask('default', ['build','watch']);
};
