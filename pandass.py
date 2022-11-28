import pandas as pd
import os


# liste des chemins input
input_path_list = [x[0] for x in os.walk('csv_input/') if x[1]==[]]


for input_path in input_path_list :
    print(input_path)
    # liste des chemins output
    output_path = input_path.replace("input","output")

    if not os.path.exists(output_path) and output_path != 'csv_output/China/Beijing/Beijing':
        os.makedirs(output_path)
    
        # ouverture input
        df_listing = pd.read_csv(input_path + '/listings.csv',encoding='latin')
        df_reviews = pd.read_csv(input_path + "/reviews.csv",encoding='latin')

        # Question 1
        if not os.path.exists(output_path+ "/df1.csv"):
            if output_path == 'csv_output/New_Zealand':
                df1 = pd.DataFrame(columns=['number_of_hosts','number_of_reviews'])
            else :
                df1= df_listing[["neighbourhood_cleansed","host_id","number_of_reviews"]]
                df1 = df1.groupby(by="neighbourhood_cleansed").agg({'host_id':'nunique', 'number_of_reviews': 'sum'}).rename(columns={'host_id' : 'number_of_hosts'})
            df1.to_csv(output_path + "/df1.csv")

        # Question 2
        if not os.path.exists(output_path+ "/df2.csv"):
            df2 = df_listing[['host_response_rate','host_acceptance_rate']]
            df2.host_acceptance_rate=df2.host_acceptance_rate.str.replace('%',"")
            df2.host_response_rate=df2.host_response_rate.str.replace('%',"")
            df2['host_response_rate']=pd.to_numeric(df2['host_response_rate'])
            df2['host_acceptance_rate']=pd.to_numeric(df2['host_acceptance_rate'])
            df2['host_response_rate']=round(df2['host_response_rate'].mean(),2)
            df2['host_acceptance_rate']=round(df2['host_acceptance_rate'].mean(),2)
            df2 = df2.head(1)
            df2.to_csv(output_path + "/df2.csv",index=False)

        # Question 3
        if not os.path.exists(output_path+ "/df3.csv"):
            l=['email', 'phone', 'work']
            d = dict()
            verif_rate = lambda i : df_listing.host_verifications.dropna().apply(lambda x : 1 if l[i] in x else 0).sum()/df_listing.shape[0]
            [d.update({l[i]:round(verif_rate(i),4)*100}) for i in range(len(l))]
            df3 = pd.DataFrame(d, index = [1])
            df3.to_csv(output_path + "/df3.csv",index=False)

        # Question 4
        if not os.path.exists(output_path+ "/df4.csv"):
            df4 = df_listing[["room_type","amenities"]]
            df4["lenght"]= df4["amenities"].dropna().apply(lambda x: x.count('"')/2)
            df4["lenght2"]= df4["lenght"]
            df4 = df4.groupby("room_type")[["lenght","lenght2"]].agg({'lenght':'mean', 'lenght2': 'std'}).rename(columns={'lenght' : 'mean', 'lenght2' : 'std'})
            df4.to_csv(output_path + "/df4.csv")

        # Question 5
        if not os.path.exists(output_path+ "/df5.csv"):
            def first_quantile(x):
                return x.quantile(0.25)
            def last_quantile(x):
                return x.quantile(0.75)

            df_listing['price'] = df_listing['price'].str.replace('$', '').str.replace(',', '').astype('float')
            df5 = df_listing.groupby('room_type')['price'].agg(['median','max','min',first_quantile,last_quantile])
            df5.to_csv(output_path + "/df5.csv")


        # Question 6
        if not os.path.exists(output_path+ "/df6.csv"):
            import numpy as np
            df6=df_listing[["bathrooms_text"]]
            df6['bathrooms_text'] = df6['bathrooms_text'].str.lower()
            df6['bathrooms_text'] = df6['bathrooms_text'].str.replace('shared half-bath','1 shared half-bath')
            df6['bathrooms_text'] = df6['bathrooms_text'].str.replace('private half-bath','1 private half-bath').str.replace('half-bath','1 half-bath')
            df6[['Number','Type']] = df6["bathrooms_text"].str.split(' ', 1, expand=True)
            df6["Number"]=df6["Number"].astype(float)
            df6=df6.dropna()
            
            dic={'bath':1, 'private':2, 'half':0.5, 'shared':0.5}
            points = lambda number,bath_type : number * np.array([dic[key] for key in list(dic.keys()) if key in bath_type]).prod()
            df6["points"] = df6[['Number','Type']].apply(lambda x : points(x[0],x[1]), axis=1)
            df6 = df6.groupby('points').count().reset_index()[['points','Number']]
            df6.to_csv(output_path + "/df6.csv", index=False)

        # Question 7
        if not os.path.exists(output_path+ "/df7.csv"):
            correlation = df_listing['description'].str.len().corr(df_listing['number_of_reviews'])
            df7 = pd.DataFrame({'Correlation': [round(correlation*100,2)]}, index = [1])
            df7.to_csv(output_path + "/df7.csv", index=False)


        # Question 8
        if not os.path.exists(output_path+ "/df8.csv"):
            df_listing_reviews = df_listing.merge(df_reviews, left_on='id', right_on='listing_id')
            nb_equal = df_listing_reviews[df_listing_reviews['host_name']==df_listing_reviews['reviewer_name']].shape[0]
            equal_percent = nb_equal/df_listing_reviews.shape[0]*100
            equal_percent = round(100*equal_percent,2)
            df8 = pd.DataFrame({'equal_percent': [equal_percent]}, index = [1])
            df8.to_csv(output_path + "/df8.csv", index=False)



