import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Latent vectors plot
def latent_vectors(model, X_train, n_comp, *args, **kwargs):

    if "color" in kwargs:
        color_ = kwargs["color"]
    else:
        color_ = "#95d5b2"


    """ Skladowe LV """
    latent_no = []
    for x in range(0, n_comp):
        latent_no.append('LV '+str(x))


    loadings = pd.DataFrame(
        model.x_loadings_, columns=latent_no, index=X_train.columns)


    col = []
    for x in range(0, len(loadings.columns)):
        for y in loadings.iloc[:, x]:
            if (y >= 0.5) or (y <= -0.5):
                col.append(color_)
            else:
                col.append('#C2CCD0')
    col2 = np.asarray(col)
    col2 = col2.reshape(loadings.shape[1], loadings.shape[0])

# vertical barplot for loadings
    y_pos = np.arange(len(loadings.index))

    for i in args:
        i
    for x in range(0, len(loadings.columns)):
        plt.subplot(1, len(loadings.columns), x+1)
        plt.barh(y_pos, loadings.iloc[:, x], color=col2[x])

        if x == 0:
            plt.yticks(y_pos, loadings.index.values)

        else:
            plt.yticks(y_pos, ['' for i in X_train.columns])

        plt.xticks([-1, -0.5, 0, 0.5, 1])
        plt.axvline(-0.5, c='gray', linestyle='--')
        plt.axvline(0.5, c='gray', linestyle='--')
        plt.grid(alpha=0.5)

        plt.xticks(fontsize=22)
        plt.yticks(fontsize=22)
        plt.title('LV'+ str(x+1), fontsize=22)

    plt.tight_layout()
    # plt.show()

# Distribution elements in LV dimnesion
def distribution_in_LVs(model, X_train, y_train, X_test, y_test, n_comp, **kwargs):
    """ Rozklad NMs w przestrzeni LV1 i LV2 """
    labels=None
    
    if "cmap" in kwargs.keys():
        cmap=kwargs["cmap"]
    else:
        cmap = 'RdYlGn_r'

    latent_no = []
    for x in range(0, n_comp):
        latent_no.append('LV '+str(x))
    loadings = pd.DataFrame(
        model.x_loadings_, columns=latent_no, index=X_train.columns)

    scores = model.x_scores_
    scores_v = model.transform(X_test)

    scores_names = list()
    for x in list(range(scores.shape[1])):
        scores_names += ('LV' + str(x+1) + ' ').split()
    scores = pd.DataFrame(
        model.x_scores_, columns=scores_names, index=X_train.index.values)

    plt.figure(figsize=(15, 12))
    plt.xlim(-1., 1.)
    plt.ylim(-1., 1.)
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=22)
    plt.grid()

    xs = model.x_scores_[:, 0]
    ys = model.x_scores_[:, 1]
    coeff = model.x_loadings_[:, [0, 1]]
    plt.xlabel('LV1',  fontsize=22)
    plt.ylabel('LV2', fontsize=22)

    xsv = scores_v[:, 0]
    ysv =  scores_v[:, 1]
    labels = None
    n = coeff.shape[0]
    scalex = 1.0/(np.max([xs.max(), xsv.max()]) -
                  np.min([xs.min(), xsv.min()]))
    scaley = 1.0/(np.max([ys.max(), ysv.max()]) -
                  np.min([ys.min(), ysv.min()]))

    plt.scatter(xs * scalex, ys * scaley, edgecolors='k',
                s=800, alpha=0.9, c=y_train,label='Training set', cmap=cmap)

    plt.scatter(xsv * scalex, ysv * scaley, edgecolors='k',
                s=800, alpha=0.9, c=y_test,label='Test set', cmap=cmap)

    if "annotate" in kwargs.keys() and kwargs["annotate"]:
        for i, txt in enumerate(X_train.index):
            plt.annotate(txt, (scalex*xs[i]+0.01, scaley*ys[i]+0.02), color = 'black', fontsize=18, alpha=0.8)
        for i, txt in enumerate(X_test.index):
            plt.annotate(txt, (scalex*xsv[i]+0.01, scaley*ysv[i]+0.02), color = 'black', fontsize=18, alpha=0.8)


    for i in range(n):
        if "arrows" in kwargs.keys() and kwargs["arrows"] == True:
            plt.arrow(0, 0, coeff[i, 0], coeff[i, 1],
                      color='#324376', alpha=0.8, head_width=0.03)

        if "annot_arrows" in kwargs.keys() and kwargs["annot_arrows"] == True:
            if labels is None:
                plt.text(coeff[i, 0] * 1.15, coeff[i, 1] * 1.15, loadings.index.values[i],
                         color='#14213d', ha='center', va='center', fontsize=16)
            else:
                plt.text(coeff[i, 0] * 1.15, coeff[i, 1] * 1.15, labels[i],
                         color='#14213d', ha='center', va='center', fontsize=16)
        else:
            pass

    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=22)

    if "title" in kwargs.keys():
        cbar.set_label(kwargs["title"], fontsize=22)
    cbar.set_alpha(1)
    cbar.draw_all()

    plt.tight_layout()
    # plt.show()
