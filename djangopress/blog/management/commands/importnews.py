import datetime
from django.core.management.base import BaseCommand, CommandError
from djangopress.blog.models import Blog, Entry, Tag, Category
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class Command(BaseCommand):
    args = ''
    help = ''

    def _import(self, post, title, timestamp, category, content):
        blogs = Blog.objects.filter(name="Site News")
        if not blogs:
            blog = Blog(name="Site News", slug=None, tagline="Codefisher.org updates and releases")
            blog.save()
            blog.sites.add(Site.objects.get(pk=1))
            blog.save()
        else:
            blog = blogs[0]
        cats = Category.objects.filter(name=category)
        if not cats:
            cat = Category(name=category, slug=slugify(category), blog=blog)
            cat.save()
        else:
            cat = cats[0]
        date = datetime.datetime.fromtimestamp(float(timestamp))
        slug = slugify(title)
        user = User.objects.get(username="michael")
        entry = Entry(title=title, pk=post, posted=date, edited=date, slug=slug,
                      author=user, edited_by=user, body=content, blog=blog,
                      visibility="VI", status="PB")
        entry.save()
        entry.categories.add(cat)
        entry.save()

    def handle(self, *args, **options):
        self._import(1,'Codefisher.org Site News','1166574060','General','<p>\r\nToday starts <a href=\"http://codefisher.org/\">testomoz.org</a> site news portal.  Watch this page for updates and news about all projects hosted on <a href=\"http://codefisher.org/\">codefisher.org</a>\r\n</p>'),
        self._import(2,'Toolbar Buttons 0.3.0.5','1169619208','Toolbar Buttons','<p>Toolbar Buttons has just been updated to  0.3.0.5 this is several versions newer that the one currently found on <a href=\"https://addons.mozilla.org/en-US/firefox/\">addons.mozilla.org</a> since there is always a delay in the update there.</p>\r\n<p>\r\nThis version contains a number of bug fixes to the language packs, along with changes to some of the bookmark button icons, since they were all using the same image.</p>\r\n<p>The next version a plan to reintroduce support for Firefox and Thunderbird 1.5 which was dropped because some of the buttons of 1.5 don\'t work in 2 and vice versa. I working on a method around this.</p>'),
        self._import(3,'Computer Words','1171181678','General','<p>I upload a poem that I wrote about <a href=\"/projects/computer_words\">Computer Words</a>. Have fun reading it.\r\n</p>'),
        self._import(4,'Button Update','1171185815','Toolbar Buttons','<p>I have updated a number of the buttons found at the <a href=\"/toolbar_button/firefox\">Firefox Button</a> page and the <a href=\"/toolbar_button/thunderbird\">Thunderbird Button</a> page.  If you have install any of these buttons it would be worth having a look at the updates.  I finally got around to making them compatible with Firefox 2.</p>'),
        self._import(5,'Site moved','1174138890','General','<p>I have moved the site from testomoz.org to <a href=\"http://codefisher.org/\">codefisher.org</a>\r\n</p>\r\n\r\n<p>There are a few reasons for this.  First I did not really like Testo that much, and the company owns the use of Testo asked me to change.</p>\r\n\r\n<p>\r\nIf you look around the site you will notice quite a number of new stuff like the <a href=\"http://codefisher.org/css/\">CSS tutorials</a>, there are 55 new pages if you look hard enough, so a lot more to read :)</p>'),
        self._import(6,'Site skin changer','1174142342','General','<p>\r\nI have added to the site a framework for easy change the whole site look and feel.  If you want to try it out go to <a href=\"/projects/site_themes\">Site Themes</a> and change from the default skin to \"Oily\".\r\n</p>\r\n\r\n<p>\r\nThere is only the default skin \"River Bank\" and \"Oily\".  I have started another one, and plan to do a few more after that is finished.\r\n</p>'),
        self._import(7,'Accessibility','1176598971','Accessibility','<p>\r\nI have become more and more involved in Firefox accessibility over the past months.  And since I think it very important, I would like to share it with you.\r\n</p>\r\n<p>\r\nI am now the web master of <a href=\"http://accessfirefox.org/\">Access Firefox</a>, a site I came across by checking out what site owner\'s, <a href=\"http://www.accessfirefox.org/AFx_About_Ken_Saunders.php\">Ken Saunders</a> email belonged to.  A funny habit I have gotten into. \r\n</p>\r\n<p>\r\nFeeling strongly that a site about accessibility should be accessible as possible, and seeing a lot of potential in it, I offered to help him fix it up. It is now had a complete make over.  And I invite every one to <a href=\"http://www.accessfirefox.org/\">Go visit it</a>\r\n</p>\r\n<p>\r\nI have also been working on accessible JavaScript widgets that use the <a href=\"http://www.w3.org/TR/wai-aria-roadmap/\">ARIA</a> (or <a href=\"http://developer.mozilla.org/en/docs/Accessible_DHTML\">Mozilla\'s page</a>) technology.\r\n</p>\r\n\r\n<p>\r\nYou can find completed examples by me in the <a href=\"http://codefisher.org/web_applications/accessibility/\"> accessibility section of Codefisher</a>\r\n</p>'),
        self._import(8,'Text Formatting Toolbar','1177412392','Toolbar Buttons','<p>\r\nI have just released a <a href=\"/format_toolbar/\">toolbar</a> for formatting text with BBcode, HTML, and Wiki code like used on Wikipedia.\r\n</p>\r\n<p>\r\nIt supports a huge amount of features, such as a <a href=\"/format_toolbar/color_picker\">color picker</a>, 19 different buttons, and a options window to charges how some of the buttons function.  And all for just 51.7KB.\r\n</p>\r\n<p>\r\nSo why not get the <a href=\"/format_toolbar/\">Text Formatting Toolbar</a>.  If you post on any forums, blogs, or help out on any Wikis it could be a huge time saver.  And yes I used it for this post.\r\n</p>'),
        self._import(25,'Sharp Color Picker Update','1208499202','Web Applications','<p>\r\n About a week ago someone contacted me about buying a copy of my <a href=\"/web_applications/color_picker/\">Sharp Color Picker</a>.  It set me thinking about ways I could improve it.  A number of things I came up with that can now be seen in the new version I have put up were.  The color pallet should be more vertical then horizontal, this puts closely related colors together more.  Some Darken and Lighten color buttons would help for fine tuning the color as could some boxes around the current color to show slight variations.  I also added a primitive color wheel, as best as could be done in HTML with out making it too slow.  Plus I made it look more presentable and fixed/improved a few minor things.  If you have not already done so it is worth having <a href=\"/web_applications/color_picker/\">another look at</a>\r\n</p>\r\n\r\n<p>\r\n Also I just put up a <a href=\"/web_applications/scroller\">image scroller</a> that looks kind of like some flash banners I have seen, expect it is all done in just HTML/JavaScript.\r\n</p>'),
        self._import(9,'ARIA Tree View','1177413654','Accessibility','<p>\r\nJust 2 posts ago I mentioned I was working  on some ARIA based projects.  ARIA means Accessible Rich Internet Applications.  Well I just managed to get another one fully functional and have cross browser support. \r\n</p>\r\n<p>\r\nIt is a <a href=\"http://codefisher.org/web_applications/accessibility/tree\">Tree View</a>, mean something that looks like what the folder do in Explorer.\r\n</p>\r\n<p>\r\nBesides just looking great, the tree view has a lot features.  Besides the basic clicking to use it, it supports fully key board usability.  You can use the arrow keys to move around the tree. \r\n</p>\r\n\r\n<p>\r\nFor any interested in other ARIA widgets I have done, there is the <a href=\"/web_applications/accessibility/slider\">Slider</a>\r\n</p>'),
        self._import(10,'0.4 beta out for testing.','1179920816','Toolbar Buttons','<p>\r\nFor those that use <a href=\"/toolbar_button/\">Toolbar Buttons</a> there is now a beta out for those that want to test it. \r\n</p>\r\n\r\n<p>\r\nThere is quite a number of improvements over past versions so it is well worth the up grade.\r\n</p>'),
        self._import(11,'Blog Bar Maker','1180008211','Images','<p>\r\nBy blog bar I mean something like this <img src=\"/af.png\" alt=\"Codefisher.org\">\r\n</p>\r\n\r\n<p>\r\nThe easy thing about this, is you jut plug in your text and colors, and 2 seconds later, you have an image.  <a href=\"http://codefisher.org/image/make_blog_bar\">Try it out</a>\r\n</p>\r\n\r\n<p>\r\nIf you find any bugs, please either <a href=\"/email\">Email Me</a> or report it here.\r\n</p>'),
        self._import(12,'AdSense Earnings','1180355850','General','<p>\r\nI have finished another extension today.  This one checks how much money you have earned with AdSense, in one click!\r\n</p>\r\n\r\n<p>\r\n<a href=\"http://codefisher.org/adsense/\">More about AdSense Earnings</a> | <a href=\"http://codefisher.org/download/adsense/adsense-1.0.1.xpi\">Download</a>\r\n</p>'),
        self._import(13,'Toolbar Buttons 0.4','1182241720','Toolbar Buttons','<p>\r\nA few days ago now <a href=\"/toolbar_button/\">Toolbar Buttons 0.4</a> was released.  It contains a number of improvements so it is strongly recommended that you upgrade to it.\r\n</p>\r\n\r\n<p>\r\nSome of the improvements include a few few buttons, support for both Firefox/Thunderbird 1.5 and 2.  An options window and a patch for Thunderbird to allow added extra buttons to it. More about it <a href=\"/toolbar_button/\">Here</a>\r\n\r\n</p>\r\n\r\n<p>The Text Formatting Toolbar was removed from it though, you can still get it though <a href=\"/format_toolbar/\">in its own extension</a>. The links in this post where added with it.\r\n</p>'),
        self._import(14,'Forum Installed','1185941392','General','<p>\r\nI have now installed a <a href=\"/forum/\">forum</a> so that it is easier for the users of my extensions to share problems and get quick help.  It should also help cut the amount of people asking the same questions, which is good for every one :)\r\n</p>'),
        self._import(15,'Toolbar Buttons 0.4.1.7','1187847495','Toolbar Buttons','<p>\r\nLast night I updated toolbar button to fix an annoying bug that was causing all the button that had drop down menus to behave wrong.  It was caused my some styling I had applied to them, that caused problems in Firefox 2, but not the Firefox 3 alphas.  To get the update go to <a href=\"/toolbar_button/\">Toolbar Button page</a>.\r\n</p>\r\n\r\n<p>\r\nThe is also the first version to be fully compatible with the <a href=\"http://codefisher.org/toolbar_button/toolbar_button_maker\">Custom Toolbar Button Maker</a>.  Previous versions had a conflict with it that caused a number of buttons (about 15) to not show up in the list of possible buttons that you could select from.\r\n</p>'),
        self._import(16,'Betas Available','1190636992','Toolbar Buttons','<p>\r\nFor those interested there is now a beta for <a href=\"/download/beta/toolbar_buttons.xpi\">Toolbar Buttons 0.45 available</a>.  The only reason it remains a beta is because it lacks all the required translations.  So if you don\'t use the English (us) version of Firefox/Thunderbird it will not work at all.  Everyone else should be able to upgrade risk free.  A list of new buttons would be as follows :\r\n</p>\r\n<ul>\r\n <li>Change Text Direction</li>\r\n <li>Toggle Animation</li>\r\n <li>Toggle Flash</li>\r\n <li>Toggle Movies</li>\r\n <li>Toggle iframes (blocks some ads)</li>\r\n <li>Toggle embedded content</li>\r\n <li>Toggle Cookies</li>\r\n <li>Switch dictionary</li>\r\n <li>Toggle Popups</li>\r\n <li>Reload Skip Cache</li>\r\n <li>Show Current Frame</li>\r\n <li>Inbox Folder</li>\r\n <li>Send & Receive</li>\r\n <li>Reply to Sender Only</li>\r\n <li>Create Filter</li>\r\n <li>Skip Trash</li>\r\n <li>Edit Draft</li>\r\n <li>Return Receipt</li>\r\n</ul>\r\n<p>\r\nThere are also a few other <a href=\"/download/beta/\">betas</a> available for download including one for the <a href=\"/download/beta/text-formatting-toolbar.xpi\">Text Formatting Toolbar</a>.  It has quite a number of new features, but none of them quite finalized.  An example of new feature is the <a href=\"/format_toolbar/custom_buttons\">custom tags</a> that allow easy creation of your own bbcode/wiki tags that are not in the default set.\r\n</p>\r\n<p>\r\nThere is also a bbcode/wiki composer for creating and storing templates, or just getting posts ready before hand.  It lacks a preview feature currently so might not be of great use.\r\n</p>\r\n<p>\r\nThere is also a beta for <a href=\"/adsense/\">AdSense Earnings</a> but that is only \"under the hood\" changes that don\'t do anything noticeable but pave the way for some big changes\r\n</p>'),
        self._import(17,'General Updates','1199519537','Toolbar Buttons','<p>\r\nIt has been a little time since I last posted anything, so a little update on what I have been doing.  Well first there has been the redesign of both this site and <a href=\"http://accessfirefox.org/\">AccessFirefox.org</a> which is owned by a friend of mine.  I also launched <a href=\"http://xrl.in\">Xrl.in</a> for the purpose of making long links shorter. \r\n</p>\r\n<p>\r\nAlong with redesigning the site I added extra content.  I added a new section called <a href=\"/tech/\">Tech Stories</a> which some may find interesting.  I also added more to my <a href=\"/css/\">CSS tutorials</a>, thought they are still not finished.\r\n</p>\r\n<p>\r\nThere is also a new section called the <a href=\"/web_applications/\">JavaScript Tory Store</a> where I have various widgets such as a <a href=\"/web_applications/color_picker/\">Color Picker</a>.  Along with a few you can add to your own site, such as a <a href=\"/web_applications/slide_over\">Slide Show</a>, <a href=\"/web_applications/center_square\">Image Loader</a> and more.\r\n</p>\r\n<p>\r\nThere has also been the official release of the Toolbar Buttons that was in its beta when I last posted.  Along with a number of bug fixes it contained over a dozen new buttons. I am now working on the next version that should again contain many new buttons. \r\n</p>\r\n<p>\r\nAlso thanks to <a href=\"http://www.smithline.net/\">Neil Smithline</a> (for the donation) this site now supports using HTTPS.  This mean I can continue supplying updates though this site (most of them go though <a href=\"https://addons.mozilla.org\">addons.mozilla.org</a>) but for example the <a href=\"/toolbar_button/toolbar_button_maker\">Custom Toolbar Button Maker</a> does not so that will continue to work under Firefox 3 which requires secure update (extension gets disabled with out it).\r\n</p>'),
        self._import(18,'SEO Toolbar','1200058296','Extensions','<p>\r\n There has just been a release of a new extension on addons.mirror.org called <a href=\"https://addons.mozilla.org/en-US/firefox/addon/6299\">SEO Toolbar</a>.  Now I think the extension is a great addition to every web masters tool kit.  Part of the reason I agreed to update and add many new features to it for the extension\'s owner <a href=\"http://www.seocompany.ca/\">SEO Company</a>\r\n</p>\r\n\r\n<p>\r\n The extension displays things like a pages PR and Yahoo! Inbound Link Count that are regarded as important when it comes to getting your pages in the top of the search results.  The extension does not just display these two results, it provides an amazing 20 different figures that every web master should check from time to time.  This includes the ILQ (Inbound Link Quality) that is unique to this extension.\r\n</p>\r\n\r\n<p>\r\n The extension also provides a handy white-list feature for controlling what sites the results are displayed on.\r\n</p>\r\n\r\n<p>\r\n So go check out its <a href=\"http://www.seocompany.ca/seo-toolbar.html\">Home page</a> and become a happy user of this extension like so many others are.\r\n</p>'),
        self._import(19,'Custom Link Buttons','1201566101','Toolbar Buttons','<p>\r\n So I have finally done what I promised quite a few people I would do.  I have made a tool for making <a href=\"http://codefisher.org/toolbar_button/link-button-maker\">Toolbar Buttons</a> that can go to any link you want.  Web site owners are allowed to put the extension\'s it creates on their own site provided they give a link back to the tool.\r\n</p>\r\n\r\n<p>\r\n It has quite a few a few options.  The URL, extension name, the button label etc. and Three methods of picking what icon the button will use.  It can be one of several supplied, the site favicon or one of your own images.  All images are resized to the correct sizes needed by the extension.\r\n</p>\r\n<p>\r\n There is also the possibility of updating the extension should you change your home page or sites icon but to do so you need the extensions id and password, which is provided when it is first created.  If you loose the password feel free to contact me and I can help you out. Updates to handle new versions of Firefox will be provided by me as well.\r\n</p> '),
        self._import(20,'AccessFirefox Reloaded','1201948410','Accessibility','<p>\r\n Anyone that has been reading many of my posts here would have seen the post titled <a href=\"http://codefisher.org/news/archive-Accessibility-7\">Accessibility</a> that was made about 9 months ago.  It was about Access Firefox.  The sites owner Ken any myself had just finished redesigning the site.  Much has changed since then.\r\n</p>\r\n<p>\r\n The site has now changed its domain name from .com to <a href=\"http://accessfirefox.org\">AccessFirefox.org</a> and further work has been done on the sites design.  There is also plenty of new content so if you have not visited the site for a while it might be worth another peak.\r\n</p>'),
        self._import(21,'Firefox Download Counter','1202293102','General','<p>\r\n Over the past few days I have finish a script that displays the number of Firefox downloads as either an image or text from a JavaScript file.  Visit <a href=\"/firefox/\">Firefox Downloads</a> to get the code snippets to insert into your own site to display the results.\r\n</p>\r\n\r\n<a href=\"http://www.spreadfirefox.com/?q=affiliates&amp;id=200351&amp;t=218\" style=\"padding:0;background-image:none;\">\r\n<img class=\"left\" src=\"/firefox/download.png\" alt=\"Firefox Downloads\">\r\n</a>\r\n\r\n<p>\r\nThe first method of displaying the download count is an image like the one of the left.  Six different colors are provided to match your sites design.  There is also the option of getting an image with just the numbers it it along with an example of how to make it overlap another image to make the two look like one.\r\n</p>\r\n\r\n<p>\r\n There is also the JavaScript option, that is really cool since it updates the number every second to follow as close as possible what the real download count would be.\r\n</p>\r\n\r\n<h3><a href=\"/web_applications/icon-getter\">Icon Getter</a></h3>\r\n\r\n<p>\r\n I have also been developing a <a href=\"/web_applications/icon-getter\">tool</a> that handles ICO (windows icons) files.  The first feature is that it can extract icons out of .EXE files.  For example it can get the Firefox logo out of the firefox.exe.  The next part of the tool is converting ICO files to PNG since they are better supported by most image editors.  And finally packaging up several PNG files into one ICO file that can be used in Windows or as your site\'s favicon.ico\r\n</p>\r\n'),
        self._import(22,'Toolbar Buttons 0.5','1204544136','Toolbar Buttons','<p>\r\n It is that time of year again, time to get ready for the next big version of Firefox.  So out comes the updates.  This on is a bit earlier than I planed so some buttons missed out on the final mix.  But there are still 16 new buttons.  You can find out from the <a href=\"/toolbar_button/button_list\">Button List</a> which ones made it.\r\n</p>\r\n\r\n<p>\r\n Toolbar buttons is now for the first time fully compatible with Firefox 3, and I managed to do it with out breaking too much in the way of Firefox 2 support.  It turned out much better than I expected.  The only ones I think I broke were the \"Read Mail\" and \"Read News\" buttons on Linux and Mac.  These functions disappeared from the tools menu is Firefox 2, and the back end for them went in Firefox 3.\r\n</p>\r\n\r\n<p>\r\n As I mentioned before this release was a bit earlier than I planed, I wanted to do a visual refresh too.  I been working on making my own icon set, and will be changing over to it soon.  Any ideas for improvements in the icons are welcome and it would be great if you could <a href=\"/email\">email</a> me them.\r\n</p>'),
        self._import(23,'An Icon set','1204549115','Images','<p>\r\n As I mentioned in the last post I am working on an icon set that will be used in Toolbar Buttons as well as my other extensions.  It is based on the <a href=\"http://www.famfamfam.com/lab/icons/silk/\">famfamfam silk</a> icon set.  Except it will have more icons, all the ones I need that it does not have, and more sizes.  The famfamfam set only has 16x16.  Below is a preview image of some of the icons.\r\n</p>\r\n\r\n<p style=\"text-align:center\">\r\n <img alt=\"Preview Image\" src=\"/images/famreloaded/preview.png\">\r\n</p>\r\n\r\n<p>\r\n  When I am ready to release the icons I will announce it in a post here.  So stay tuned, and <a href=\"/news/feed\">subscribe to the feed</a> to keep up to date.\r\n</p>'),
        self._import(24,'New Extension Releases','1206749126','Extensions','<p>\r\n Just in the past two days I have released one new extension and an update to another.  Both of which warrant a mention.\r\n</p>\r\n\r\n<p>\r\n <a href=\"/projects/send-page\">Send Page via Email</a> is designed to bring a feature that is in IE into Firefox.  As with every IE feature it can be used as a reason not to use Firefox, even if it does everything else so much better.  When the menu item for it, that can be found in the tools menu, is click it opens up the default mail client with an attachment of the current page.  Depending on what email client the recipient uses the web page will normally be displayed in the message body when it is received.\r\n</p>\r\n\r\n<p>\r\n Also there has been another update to <a href=\"/toolbar_button/\">Toolbar Buttons</a> in which a number of reported bugs were resolved.  The changes where\r\n</p>\r\n\r\n <ul>\r\n  <li>Fixed the page zoom buttons for Firefox 3</li>\r\n  <li>Fixed a typo in the \'Toggle Read\' buttons\' tooltip</li>\r\n  <li>Fixed a bug in the Real Next/Previous button</li>\r\n  <li>Reverted the implementation of the Read Mail/News buttons to be more reliable in Firefox 2.  The Firefox 3 betas still use the less reliable implimention.</li>\r\n  <li>Fixed a few other minor errors that were thrown when some buttons were not in use.</li>\r\n </ul>'),
        self._import(26,'Pastel SVG Icons','1208521641','Images','<p>\r\n A few posts back I mentioned that I was in the process of producing an icon set that I intend to use in my extensions, and also make a Firefox and Thunderbird theme out of. I have now uploaded the set and you can get them from the <a href=\"http://codefisher.org/pastel-svg/\">Pastel SVG Icons</a> home page.   There are almost 500 icons, my target is somewhere in the 1250 range, so that is not quite half way.\r\n</p>'),
        self._import(27,'Text Formatting Toolbar 0.1.4','1208594721','Extensions','<p>\r\n I have finally released <a href=\"/format_toolbar/version/0.1.4\">version 0.1.4</a> of the <a href=\"/format_toolbar/\">Text Formatting Toolbar</a>.  It has a lot of little fixes that needed to be done along with two major new features.\r\n</p>\r\n\r\n<p>\r\nI have been asked to include a number of less common tags.  I have now implemented a way of creating your own.  To find out more about it you can read my <a href=\"/format_toolbar/custom_buttons\">tutorial</a>\r\n</p>\r\n\r\n<p>\r\n There is also a feature that is used to create and store posts the can be then used as a template/canned reply etc.  It is also great because it gives you a backup of the post, and a friendly environment in which to write it.  Some people have found other uses for it, such as a note taker.\r\n</p>\r\n\r\n<p>\r\n The other change to the extension was I changed all the icons to those I had created for the  <a href=\"/pastel-svg/\">Pastel SVG</a> icon set.\r\n</p>'),
        self._import(28,'Toolbar Buttons 0.5.0.4','1208600779','Toolbar Buttons','<p>\r\n Another update of Toolbar Buttons has been released.  It fixed a number of minor issues that had been reported in the previous release.  There where no major changes though.\r\n</p>\r\n\r\n<p>\r\n The think it should be the last one in the 0.5.0 branch of Toolbar Buttons.  The next release should be 0.5.5 unless any unexpected bugs are found.  The plans for 0.5.5 is to start to change the icons and add the next 15 or so wanted buttons.\r\n</p>'),
        self._import(29,'Update Time!!','1213604948','Extensions','<p>\r\n  <a href=\"/toolbar_button/\">Toolbar Buttons</a>, <a href=\"/format_toolbar/\">Text Formatting Toolbar</a> and <a href=\"/projects/xrl.in\">Xrl.in Tiny Links</a> all got an update for Firefox 3 which is supposed to come out on the 17th of June (that is today as I write this post).  All three extensions received a number of bug fixes as well, some Firefox 3 related others not.\r\n</p>\r\n<p>\r\n  I have not updated Minimize To Tray <strong>Enhancer</strong> as its dependency has not been updated (it looks like I might have to look into doing that if I can).  All the other extensions of mine are little used and need major work so I am not inclined to update them yet.  I will do so eventually, would be great if someone else helped out though ;)\r\n</p>'),
        self._import(30,'Version 0.6 - a bug fix & a little new','1222694497','Toolbar Buttons','<p>\r\n I have finally finished version 0.6 of Toolbar Buttons.  I think I fixed more bugs in this release then any other I have done.  Manly because I kept putting off releasing it; for two reasons.  One was I could not find a few hours together to release it (normally takes about 3 or so hours once everything is take into account).  Plus I made changes that meant I had to update the Custom Toolbar Button Maker.\r\n</p>\r\n\r\n<p>\r\n I now have a week off, so I finished of Toolbar Buttons and rewrote the  Custom Toolbar Button Maker; that was a lot of fun, been itching to do it.  After studying SQL for 6 months I manged it make it a lot faster, and a lot less code, almost 400 lines shorter.  400 lines that can\'t possibly have bugs in it.\r\n</p>\r\n\r\n<p>\r\n There are eight new buttons, much fewer that I would have liked.  The request list has grown much more than that.\r\n</p>'),
        self._import(33,'Toolbar Buttons 0.6.0.5','1238327526','Toolbar Buttons','<p>\r\n The next version of <a href=\"/toolbar_button/\">toolbar buttons</a> is out.  Unfortunately it does not contain all the new things I would have liked, only the <a href=\"/toolbar_button/version/0.6.0.5\">fixes</a> to all the bugs reported over the past few months.  I was distracted with other projects that resulted in much less being done with my extensions then I had hoped over the long summer holidays.\r\n</p>\r\n\r\n<p>\r\n I am almost ready to do releases on some of my other extensions so stay tuned for more.\r\n</p>'),
        self._import(34,'Xrl.in Tiny Links 1.4','1240218804','Extensions','<p>\r\n There is now a new version of the <a href=\"http://codefisher.org/projects/xrl.in.php\">Xrl.in Tiny Links</a> extension which you can <a href=\"http://codefisher.org/download/tiny-links/xrl.in-1.4.xpi\">downloaded</a>. <a href=\"http://xrl.in/\">Xrl.in</a> is link shorting service that is part of the <a href=\"http://codefisher.org/\">Codefisher.org</a> network.\r\n</p>\r\n\r\n<p>\r\n The changes in this version include streamlining the the extension by removing the drop down from the button. All the settings can be still found in the option\'s window.  To to <strong>Tools</strong> menu then <strong>Add-ons</strong>; in the <strong>Extensions</strong> tab you will find the extension and be able to open it\'s options. Another change is that once the button, which is located inside the url bar, is clicked the url is automatically copied to the clipboard, though this can be turned off.\r\n</p>\r\n\r\n<p>\r\nThe extension also added support for <a href=\"http://group.xrl.in/\">Xrl.in link Groups</a>, if you right click on the tab bar you can create a link group of all the currently open tabs.\r\n</p>'),
        self._import(35,'Text Formatting Toolbar 0.1.4.10','1240655457','Extensions','<p>\r\n The next version of the <a href=\"http://codefisher.org/format_toolbar/\">Text Formatting Toolbar</a> has been released, <a href=\"http://codefisher.org/format_toolbar/version/0.1.4.10\">version 0.1.4.10</a>.  The changes are minor, only the little bugs reported over the past few months.\r\n</p>'),
        self._import(36,'MinimizeToTray Plus 1.0','1248180500','Extensions','<p>\r\n Long promised, but I finally merged MinimizeToTray into my Minimize To Tray Enhancer.  And to celebrate I renamed it <a href=\"/minimizetotray/\">MinimizeToTray Plus</a>.\r\n</p>\r\n\r\n<p>\r\n It has all the features of MinimizeToTray built in now.  I also fixed up the -turbo mode which was promised for that extension by its original developers.  MinimizeToTray Plus now uses this internally to simplify some things like its ability load an application minimize at startup.\r\n</p>\r\n\r\n<p>\r\n I also did some changes to the internal API, so I can now add features like always showing the tray icon, and just showing a single icon.  These features where imposable before.\r\n</p>\r\n\r\n<p>\r\n Disappointedly there is still a major glitch in the extension.  In Firefox 3.5 the icons can\'t display their menus when clicked.  This is because of <a href=\"https://bugzilla.mozilla.org/show_bug.cgi?id=502457\">bug 520457</a> which I would ask everyone to visit and vote on.\r\n</p>\r\n\r\n<p>\r\n I have also made the code for the extension <a href=\"http://svn.codefisher.org/svn/\">avilable online</a>.  Though this is of very little interest to most, I am looking for someone to help port the extension to Mac.  I am about to start work on a Linux port.\r\n</p>'),
        self._import(37,'Toolbar Buttons 0.6.0.6','1250850989','Toolbar Buttons','<p>\r\nVersion <a href=\"toolbar_button/version/0.6.0.6\">0.6.0.6</a> of Toolbar Buttons is now out.\r\nThe changes are:\r\n</p>\r\n<ul>\r\n <li>Bug fixed in the undo and redo buttons in Thunderbird.</li>\r\n <li>Close all tabs does not close the window in Firefox 3.5</li>\r\n\r\n <li>Minimum and maximum application versions raised and some old compatibility code dropped.</li>\r\n <li>Bookmark menu buttons improved, drag and drop now works.</li>\r\n <li>Page zoom buttons now works in the Thunderbird 3 betas</li>\r\n <li>Empty Trash button now works in Thunderbird 3 betas</li>\r\n <li>Next/Previous tab buttons in Firefox now loop around</li>\r\n <li>Add-ons window can now be opened in a tab when middle clicked.</li>\r\n\r\n <li>Some locales updated, thanks to the babelzilla team.</li>\r\n</ul>\r\n'),
        self._import(38,'MinimizeToTray Plus 1.0.7','1258941307','Extensions','<p>\r\nWith version 1.0.7 I can finally safely say that I have made the extension stable.  Mainly because of <a href=\"https://bugzilla.mozilla.org/show_bug.cgi?id=502457\">bug 502457</a> which stops menus (such as the one for the tray icon) from showing when a window is minimized. Having finally resolved that, I have finished all the other work that extension badly needed.\r\n</p>\r\n\r\n<p>\r\n See the <a href=\"http://codefisher.org/minimizetotray/\">MinimizeToTray Plus home page</a> for more information.\r\n</p>'),
        self._import(39,'Toolbar Buttons 1.0 beta','1261485609','Toolbar Buttons','<p>\r\nI have got a beta of the 1.0 version of Toolbar Buttons out.  I have made a rather lengthly <a href=\"http://codefisher.org/forum/viewtopic.php?id=558\">post on the forum</a> about it for anyone interested in more information.\r\n</p>'),
        self._import(40,'MinimizeToTray Plus 1.0.8','1265808306','Extensions','<p>\r\n Earlier this week <a href=\"/minimizetotray/\">MinimizeToTray Plus</a> version <a href=\"/minimizetotray/version/1.0.8\">1.0.8</a> was released.  It fixed quites a number of little problems that user were experiencing.  You can see a full list of the updates in the <a href=\"/minimizetotray/version/1.0.8\">version notes</a>\r\n</p>'),
        self._import(41,'Xrl.in Tiny Links 1.5','1265808618','Extensions','<p>\r\n Version 1.5 of <a href=\"/projects/xrl.in\">Xrl.in Tiny Links</a> is out. It includes a few new locales, an also now makes its icon animated when busy. For those not aware it uses my <a href=\"http://xrl.in/\">Xrl.in</a> link shortening service to create links the are tiny in length.  It adds a single icon into the url bar next to the go button.\r\n</p>')
        self._import(43,'Toolbar Buttons 1.0','1296566360','Toolbar Buttons','<p>\r\nI have finally got <a href=\"http://codefisher.org/toolbar_button/version/1.0\">Version 1.0</a> of Toolbar Buttons out.  It finally brings the extension up to speed with supporting the latest releases of Firefox and Thunderbird.\r\n</p>\r\n\r\n<p>\r\nThe extension also got a visual refresh, it is now using my own icon set.  Though some of the icons still need work (particular those of the larger icon size) it has been mostly fixed up.\r\n</p>\r\n\r\n<p>\r\nAlso quite importantly, and what has taken the most time with this release, is the extension had large internal changes.  It is now much easier to add new stuff, and keep track of what buttons are their.  Already encouraging some people to <a href=\"http://codefisher.org/toolbar_button/contributing\">contribute</a> new buttons to the extension.  It also opens the possibility of doing some exciting stuff with the Custom Toolbar Button maker, at least as soon as I get that updated.\r\n</p>\r\n\r\n<p>\r\n  Apologies to everyone getting this via email and received the previous one horribly mangled.\r\n</p>')