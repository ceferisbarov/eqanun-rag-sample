EMAIL_REGEX= '(\S+@\S+)'
URL_REGEX = "((?:w{3}.)?[a-zA-Z0-9ƏİŞĞÖÜIÇəi̇şğöüçı]+?\.(?:com|net|org|edu|gov|asia|cat|info|int|jobs|mobi|museum|name|post|pro|tel|travel|ai|az|biz|et|eu|fr|ne|ru|sh|tr|tv|ua|uk|us|ws))"
NUMBER_WITH_DOT = '((?:\d+\.){1,}\d+)'
EXCEPTIONS = '((?:və s.|ve s.|\.{2,})(?=\s*[«"!#$%&\'()*+,\/:;<=>?@[\\]^_`{\|}~-]*\s*[a-zəi̇şğöüçı])|Sov\.)'
FILE_NAMES = '([^\s]+\.(?:csv|txt|html|xml|jpg|class|java|cvs|doc|docx|exe|gif|htm|html|jpg|jpeg|pdf|png|ppt|pptx|tar|wav|xls|xlsx|zip))'