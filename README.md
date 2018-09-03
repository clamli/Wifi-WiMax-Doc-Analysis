## Python Crawler

Crawl 802.11and 802.16 from the following five links,

1. [802.11 after 2000](https://mentor.ieee.org/802.11/documents)
2. [802.11 before 2000](http://grouper.ieee.org/groups/802/11/Documents/DocumentArchives/)
3. [802.16 after 2012](https://mentor.ieee.org/802.16/documents)
4. [802.16 before 2012, IEEE 802.16 Documents](http://www.ieee802.org/16/docs/index.html#contrib)
5. [802.16 before 2012, IEEE 802.16 Completed Projects](http://www.ieee802.org/16/tgs.html)



### \# Attributes of Saved Tables 

- 802.11

| Create Time        | Upload Time                 | DCN  | Rev    | Group  | Title  | Author           | File Link | Additional File Link |
| :----------------- | :-------------------------- | :--- | ------ | ------ | ------ | ---------------- | --------- | -------------------- |
| String: yyyy-mm-dd | String: yyyy-mm-dd hh:mm:ss | int  | String | String | String | String: A;B or A |           | DOC ONLY             |

- 802.16 after 2012

| Create Time        | Upload Time                 | DCN  | Rev    | Group  | Title  | Author           | File Link |
| ------------------ | --------------------------- | ---- | ------ | ------ | ------ | ---------------- | --------- |
| String: yyyy-mm-dd | String: yyyy-mm-dd hh:mm:ss | int  | String | String | String | String: A;B or A | String    |

- 802.16 before 2012, IEEE 802.16 Documents

| Official/Contribution           | Time               | Title  | Author           | File Link | Additional Information                       |
| ------------------------------- | ------------------ | :----- | ---------------- | --------- | -------------------------------------------- |
| int: Official-0, Contribution-1 | String: yyyy-mm-dd | String | String: A;B or A | String    | String (from file download address to title) |

- 802.16 before 2012, IEEE 802.16 Completed Projects

| Category1 | Category2 | Task Group/Contributed           | Session Info                                      | Title  | Author           | Time               | File Link |
| --------- | --------- | -------------------------------- | ------------------------------------------------- | ------ | ---------------- | ------------------ | --------- |
| String    | String    | int: Task Group-0, Contributed-1 | String (Only exists in the contributed documents) | String | String: A;B or A | String: yyyy-mm-dd | String    |



### \# NOTICE

1. Empty value should be set to **null**.
2. Author name may contain "Approved". (IEEE 802.16 Documents)
3. Time format is only XXXX-XX-XX  /  XX/XX/XX, and we use the **last time** that satisfies the regulation expression as the time of a document. (IEEE 802.16 Documents & IEEE 802.16 Completed Projects)
4. Information **after** time should be included in Title.  (IEEE 802.16 Documents & IEEE 802.16 Completed Projects)
5. Author names should be the names in the parenthesis **('()')**.  (IEEE 802.16 Documents & IEEE 802.16 Completed Projects)