CKEDITOR.replace('body', {
    language: 'ru',
    extraPlugins: 'image2,uploadimage,codesnippet',
    removePlugins: 'easyimage,cloudservices',
    filebrowserUploadUrl: '/upload/',
    filebrowserUploadMethod: 'form',
    height: 400,
    width: 'auto',
    autosave: {
        saveDetectionSelectors: "form input[type='submit']",
        delay: 10
    },
    allowedContent: true,
    contentsCss: '/static/css/ckeditor_contents.css',
    bodyClass: 'document-editor',
    placeholder: 'Введите текст вашего поста здесь...',
    toolbar: [
        { name: 'clipboard', items: ['Cut', 'Copy', 'Paste', 'Undo', 'Redo'] },
        { name: 'styles', items: ['Styles', 'Format'] },
        { name: 'basicstyles', items: ['Bold', 'Italic', 'Strike', 'Underline'] },
        { name: 'paragraph', items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'] },
        { name: 'links', items: ['Link', 'Unlink'] },
        { name: 'insert', items: ['Image', 'Table', 'HorizontalRule', 'SpecialChar'] },
        { name: 'document', items: ['Source'] },
        { name: 'codesnippet' }
    ]
});
