# if you want support for tinymce in the admin pages
# add tinymce to the installed apps (after installing if needed)
# and then import these settings, or copy and adjust as needed

TINYMCE_DEFAULT_CONFIG = {
    'relative_urls': False,
    'plugins': "table code image link colorpicker textcolor wordcount",
    'tools': "inserttable",
    'toolbar': "undo redo | styleselect | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | forecolor backcolor",
    'extended_valid_elements': 'script[language|type|src],events[template|start],#gallery[class|id|show_description|show_title|count|slider],#show_blog_latest[class|id|words|images|blog|count]'
}
TINYMCE_JS_URL = "/static/js/tinymce/tinymce.min.js"