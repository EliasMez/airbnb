import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# liste des chemins input
input_path_list = [x[0] for x in os.walk('csv_input/') if x[1]==[]]


for input_path in input_path_list :
    input_path += '/'
    print(input_path)
    # liste des chemins output
    output_path = input_path.replace("input","output")
    visu_path = input_path.replace("csv_input","visu")

    if output_path != 'csv_output/China/Beijing/Beijing/' :
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        if not os.path.exists(visu_path):
            os.makedirs(visu_path)
    
        # ouverture input
        df_listing = pd.read_csv(input_path + 'listings.csv',encoding='latin')
        df_reviews = pd.read_csv(input_path + "reviews.csv",encoding='latin')

        # Question 1
        if not os.path.exists(output_path+ "df1.csv"):
            if output_path == 'csv_output/New_Zealand/':
                df1 = pd.DataFrame(columns=['number_of_hosts','number_of_reviews'])
                fig, ax = plt.subplots(figsize=(10, 5))
                plt.savefig(visu_path + "df1.png", bbox_inches='tight')

            else :
                df1= df_listing[["neighbourhood_cleansed","host_id","number_of_reviews"]]
                df1 = df1.groupby(by="neighbourhood_cleansed").agg({'host_id':'nunique', 'number_of_reviews': 'sum'}).rename(columns={'host_id' : 'number_of_hosts'})
                df1 = df1.reset_index()
                city = visu_path.split('/')[-1]


                x = np.arange(len(df1.neighbourhood_cleansed.unique()))  # the label locations
                width = 0.4 

                fig, ax = plt.subplots(figsize=(28, 12))
                # fig.set_size_inches(8, 6)

                rects1 = ax.bar(x - (width/2 + 0.00) , df1.number_of_hosts, width, label="number_of_hosts")
                rects2 = ax.bar(x + (width/2 +0.00) , df1.number_of_reviews/100 , width, label="number_of_reviews X 100")

                # Add some text for labels, title and custom x-axis tick labels, etc.
                ax.set_title("Nombre d'hôtes et de commentaires par quartier")
                ax.set_xticks(x, df1.neighbourhood_cleansed.unique())
                ax.set_xlabel("Quartiers de " + city)
                ax.title.set_size(40)
                ax.xaxis.label.set_size(25)
                ax.yaxis.label.set_size(25)
                plt.xticks(fontsize=15)
                plt.yticks(fontsize=15)
                ax.legend(fontsize=15)

                ax.set_xticklabels(df1.neighbourhood_cleansed.unique(), rotation=80, ha='right')

                fig.tight_layout()
                plt.savefig(visu_path + "df1.png", bbox_inches='tight')
            df1.to_csv(output_path + "df1.csv",index=False)


            

        # Question 2
        if not os.path.exists(output_path+ "df2.csv"):
            df2 = df_listing[['host_response_rate','host_acceptance_rate']]
            df2.host_acceptance_rate=df2.host_acceptance_rate.str.replace('%',"")
            df2.host_response_rate=df2.host_response_rate.str.replace('%',"")
            df2['host_response_rate']=pd.to_numeric(df2['host_response_rate'])
            df2['host_acceptance_rate']=pd.to_numeric(df2['host_acceptance_rate'])
            df2['host_response_rate']=round(df2['host_response_rate'].mean(),2)
            df2['host_acceptance_rate']=round(df2['host_acceptance_rate'].mean(),2)
            df2 = df2.head(1)
            df2.to_csv(output_path + "df2.csv",index=False)

        
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

            data=[df2.host_acceptance_rate.mean(),100.0-df2.host_acceptance_rate.mean()]
            labels=["Acceptation","Refus"]
            color = sns.color_palette("bright")

            ax1.pie(data,labels=labels,colors=color,autopct='%.0f%%',textprops={'fontsize':22})
            ax1.set_title("Moyenne d'acceptations des hotes")
            ax1.title.set_size(30)

            data=[df2.host_response_rate.mean(),100.0-df2.host_response_rate.mean()]
            ax2.pie(data,labels=labels,colors=color,autopct='%.0f%%',textprops={'fontsize':22})
            ax2.set_title("Moyenne d'acceptations des reviewers")
            ax2.title.set_size(30)
            plt.savefig(visu_path + "df2.png", bbox_inches='tight')


        # Question 3
        if not os.path.exists(output_path+ "df3.csv"):
            l=['email', 'phone', 'work']
            d = dict()
            verif_rate = lambda i : df_listing.host_verifications.dropna().apply(lambda x : 1 if l[i] in x else 0).sum()/df_listing.shape[0]
            [d.update({l[i]:round(verif_rate(i),4)*100}) for i in range(len(l))]
            df3 = pd.DataFrame(d, index = [1])
            df3.to_csv(output_path + "df3.csv",index=False)

            plt.figure(figsize=(15,8))
            plt.bar(df3.columns,df3.iloc[0].sort_values())
            plt.title("Le nombre d’host par quartier")
            plt.xlabel("neighbourhood_cleansed")
            plt.ylabel("number_of_hosts")
            plt.savefig(visu_path + "df3.png", bbox_inches='tight')


        # Question 4
        if not os.path.exists(output_path+ "df4.csv"):
            df4 = df_listing[["room_type","amenities"]]
            df4["lenght"]= df4["amenities"].dropna().apply(lambda x: x.count('"')/2)
            df4["lenght2"]= df4["lenght"]
            df4 = df4.groupby("room_type")[["lenght","lenght2"]].agg({'lenght':'mean', 'lenght2': 'std'}).rename(columns={'lenght' : 'mean', 'lenght2' : 'std'})
            df4=df4.reset_index()
            df4.to_csv(output_path + "df4.csv",index=False)

            plt.figure(figsize=(10,5))
            sns.catplot(kind="bar",data=df4,x='room_type',y='mean')
            plt.title("Moyenne et écart type des équipements par type de salle")
            plt.errorbar(df4.room_type, df4["mean"],yerr= df4["std"], fmt = 'none', capsize = 8, ecolor = 'black', elinewidth = 2, capthick = 4)
            plt.savefig(visu_path + "df4.png", bbox_inches='tight')


        # Question 5
        if not os.path.exists(output_path+ "df5.csv"):
            def first_quantile(x):
                return x.quantile(0.25)
            def last_quantile(x):
                return x.quantile(0.75)

            df_listing['price'] = df_listing['price'].str.replace('$', '').str.replace(',', '').astype('float')
            df5 = df_listing.groupby('room_type')['price'].agg(['median','max','min',first_quantile,last_quantile])
            df5.to_csv(output_path + "df5.csv",index=False)

            plt.figure(figsize=(10,5))
            sns.boxplot(x="room_type", y="price" ,data=df_listing, showfliers=False)
            plt.title("Moyenne des équipements par type de salle")
            plt.savefig(visu_path + "df5.png", bbox_inches='tight')


        # Question 6
        if not os.path.exists(output_path+ "df6.csv"):
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
            df6.to_csv(output_path + "df6.csv", index=False)

            plt.figure(figsize=(15,7))
            sns.histplot(x="Number",data=df6,bins=30)
            plt.title("Moyenne des équipements par type de salle")
            plt.savefig(visu_path + "df6.png", bbox_inches='tight')


        # Question 7
        if not os.path.exists(output_path+ "df7.csv"):
            correlation = df_listing['description'].str.len().corr(df_listing['number_of_reviews'])
            df7 = pd.DataFrame({'Correlation': [round(correlation*100,2)]}, index = [1])
            df7.to_csv(output_path + "df7.csv", index=False)

            plt.figure(figsize=(10,5))
            plt.scatter(df_listing['description'].str.len(),df_listing['number_of_reviews'])
            plt.title("Corrélation entre le nombre de reviews et la taille de la description en termes de nombre de caractères")
            plt.xlabel("nombre de caractères par description")
            plt.ylabel("number_of_reviews")
            plt.savefig(visu_path + "df7.png", bbox_inches='tight')


        # Question 8
        if not os.path.exists(output_path+ "df8.csv"):
            df_listing_reviews = df_listing.merge(df_reviews, left_on='id', right_on='listing_id')
            nb_equal = df_listing_reviews[df_listing_reviews['host_name']==df_listing_reviews['reviewer_name']].shape[0]
            equal_percent = nb_equal/df_listing_reviews.shape[0]*100
            equal_percent = round(100*equal_percent,2)
            df8 = pd.DataFrame({'equal_percent': [equal_percent]}, index = [1])
            df8.to_csv(output_path + "df8.csv", index=False)



