import matplotlib.pyplot as plt
import seaborn as sns




class EDA():

    def __init__(self, df):
        self.df = df

    def KDE_PLOT(self):
        # kernel density estimate plot - all hurricanes
        ax_kde = sns.displot(
            data=self.df,
            x="norm_date", hue="class_label",
            kind="kde", height=5, aspect=1.5,
            multiple="fill", clip=(0, None)
        ).set(title='KDE plot_all hurricanes', xlabel='Time frame(0-100)', ylabel='Density')
        return ax_kde       
