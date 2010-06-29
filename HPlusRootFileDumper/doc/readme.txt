**************************************************
*                                                *
* How to create the automated doxygen manual     *
*                                                *
* Note: This is a crude/rough guide. People that *
*       know more should edit this file!         *
**************************************************
Before the manual can be generated, edit the "doxygen.config" file and
edit it accordingly. Specifically, on line 33 you have to define the
*path where the manual will be created in.
1) |myTerinal> emacs doxygen.config
2) |myTerinal> source createref.(c)sh
