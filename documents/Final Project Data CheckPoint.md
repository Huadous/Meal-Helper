# Final Project Data CheckPoint

#### Project code

https://github.com/Huadous/final-project

#### Data sources

*Categories information*

*   Origin : 

    [Documentation](https://www.yelp.com/developers/documentation/v3/all_category_list)

    [Download](https://www.yelp.com/developers/documentation/v3/all_category_list/categories.json)

    <img src="/Users/huayu/Documents/canvas/finalproject/documents/images/image-20210418195907447.png" alt="image-20210418195907447" style="zoom:50%;" />

*   Format :  JSON( > 1000 records [$\approx 1500$])

*   The file can be downloaded directly without additional verification methods, I used cache.

*   The function of this file is that it contains information about the types of restaurants, and it also provides information for which countries are searchable. Therefore, the category data file can be used as a benchmark for restaurant category search. Because this is an all-category file, which contains not only the categories of restaurants. What I need to do is to filter out the category information of the restaurant from all categories.

    There are about 1,500 categories in this file. I need to download all of them and filter out the restaurant categories. The category of the restaurant is 192.

*   Code : <img src="/Users/huayu/Documents/canvas/finalproject/documents/images/image-20210418194300556.png" alt="image-20210418194300556" style="zoom:50%;" />

    Snapshot:

    <img src="/Users/huayu/Documents/canvas/finalproject/documents/images/image-20210418194348984.png" alt="image-20210418194348984" style="zoom:50%;" />

*ISO 3166-1 alpha-2 code*

*   Origin :

    [Documentation](https://datahub.io/core/country-list)

    [Download](https://datahub.io/core/country-list/r/data.json)

    <img src="/Users/huayu/Documents/canvas/finalproject/documents/images/image-20210418195845643.png" alt="image-20210418195845643" style="zoom:50%;" />

*   Format :  JSON( < 1000 records [$\approx250$])

*   The file can be downloaded directly without additional verification methods, I used cache.

*   Because in the previous category file, there will be information about different restaurant categories in which countries provide search services. Therefore, it is necessary to use the abbreviations of the names of each country in this file to determine whether the restaurant in this category can be searched in the United States, which can reduce the time wasted due to unnecessary searches, especially in the case of a bad network important.

*   Code : <img src="/Users/huayu/Documents/canvas/finalproject/documents/images/image-20210418195102681.png" alt="image-20210418195102681" style="zoom:50%;" />

    Snapshot :<img src="/Users/huayu/Documents/canvas/finalproject/documents/images/image-20210418195157770.png" alt="image-20210418195157770" style="zoom:50%;" />

*United States Cities Database*

*   Origin :

    [Documentation](https://simplemaps.com/data/us-cities)

    [Download](https://simplemaps.com/static/data/us-cities/1.73/basic/simplemaps_uscities_basicv1.73.zip)

    <img src="/Users/huayu/Documents/canvas/finalproject/documents/images/image-20210418201442342.png" alt="image-20210418201442342" style="zoom:50%;" />

    <img src="/Users/huayu/Documents/canvas/finalproject/documents/images/image-20210418201420628.png" alt="image-20210418201420628" style="zoom:50%;" />

*   Format : CSV ( >1000 records [$\approx 28000$])
*   The file can be downloaded directly without additional verification methods, I didn't use cache. I just add it into the source file and will provide it with my program together.

*Using API key to get base information and do analysis*

*Crawling and scraping multiple pages in Yelp to gain information related covid-19*

