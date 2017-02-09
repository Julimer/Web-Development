Python Version: Python 3.5.2

Global stream page: <-login or registered
- When the user add a new post, the page will refresh to show his/her post instantly; when others has some new post, it will use AJAX to partially update the page every 5 seconds.
- When a comment is added, it will be appended to the post by AJAX.
- In the right side of navigation bar, there are "Person Image"(link to the person profile), "Edit"(link to Edit profile page), "Heart"(Link to Follow stream), "Bell"(No function yet), "Logout"(for logging current user out)
- The "PERSON" image icon in the listed posts is linking to that person's profile. CLICK IT!
- All posts that have been posted in reverse-chronological order.


Follow Stream page: <- click the "HEART" on global stream page
- The new posts are not updating every 5 seconds, because I think the periodically updating functions are actually not very pleasant in real life. It is actually better to let the user refresh it by their desires.
- When a comment is added, it will be appended to the post by AJAX.
- Show the posts of your followings in reverse-chronological order.


Profile page (FOLLOW/UNFOLLOW): <- Click the person image icon!
- The new posts are not updating every 5 seconds, because I think the periodically updating functions are actually not very pleasant in real life. It is actually better to let the user refresh it by their desires.
- When a comment is added, it will be appended to the post by AJAX.
- The person's profile is shown in the left bar.
- By clicking the "Follow"/"Unfollow" button, you can follow/unfollow this person.
- If trying to go to ".../profile/100000" in which the id=100000 actually does not exist, the page will be redirected to the global stream page.
- The "Grumblr" or the "HOME" icon in the navigation bar will direct back to the global stream page.

