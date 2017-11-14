// See http://brunch.io for documentation.
exports.paths = {
    public: 'media/public/',
    watched:["media/app/"]
}



exports.files = {
  javascripts: {joinTo: 'app.js'},
  stylesheets: {joinTo: 'app.css'}
};

exports.plugins = {
    browserSync: {
        files:["**/*.{scss,css,html,py,js}"],
        proxy:'localhost:8000',
        reloadDebounce:3000,
          logLevel: "debug"
    }
};

exports.npm = {
    styles: {
        'css-spaces': ["dist/spaces.min.css"],
        'bulma': ["css/bulma.css", 'css/bulma.css.map']
    }
};
