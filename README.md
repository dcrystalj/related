# blogs recommendation system


## Do you want to include related blog posts to your blog?

This system is now built for wordpress blogs only, but can be easly extended to any blog type. For different blog type parse_posts.py needs to be rewritten.

- To add recommendations to your wordpress blog you need to:
    * Create database X
    * In wordpress/reccommend_db.py change values according to [X, username, password]
    * uncommend line ```db.create_tables([Reccommend])``` in ```wordpress/reccommend_db.py``` run this script and comment it again. This will create reccommend table in your database.
    * In php/api.php change values according to your database as well
    * run ```python reccomend url_of_your_blog```. this will do save related posts for each of your bost post
    * add
    ```
    <div style="width: 100%">
        <div>Related:</div>
        <iframe src='PUBLIC_LINK_TO_YOUR_PHP_FOLDER/api.php?link=<?php the_permalink(); ?>&blog=<?php echo site_url(); ?> '></iframe>
    </div>
    ```

    to your ```WORDPRESS_FOLDER\wp-content\themes\NAME_OF_YOUR_THEME\content.php``` insde of ```<div class="entry-content"></div>``` block at the end.

- To see in pictures how alghoritm works on your blog run ```analyse_algorithm BLOG_URL BLOG_NAME```

- To check for new post run ```check_new_post.py``` and setup you automative reccommendation.

- To copy random wordpress blog to you local blog for testing, use ```parse_wordpress_blog.py``` script