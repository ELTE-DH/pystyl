from __future__ import print_function

import os

from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from bokeh.models import HoverTool, ColumnDataSource, Axis
from bokeh.plotting import figure, show, output_file, save


std_output_path = os.path.dirname(os.path.abspath(__file__))+'/../output/'

def scatterplot_2d(X, sample_names, feature_names, target_ints=None, target_idx=None,
                   outputfile=std_output_path+'2d.pdf', nb_clusters=0, loadings=None): 
    sns.set_style('dark')
    sns.plt.rcParams['axes.linewidth'] = 0.4
    fig, ax1 = sns.plt.subplots()  

    # first plot slices:
    x1, x2 = X[:,0], X[:,1]
    ax1.scatter(x1, x2, 100, edgecolors='none', facecolors='none')
    if nb_clusters:
        # clustering on top (for colouring):
        clustering = AgglomerativeClustering(linkage='ward', affinity='euclidean', n_clusters=nb_clusters)
        clustering.fit(X)
        # add slice names:
        for x, y, name, cluster_label in zip(x1, x2, sample_names, clustering.labels_):
            ax1.text(x, y, name, ha='center', va="center",
                     color=plt.cm.spectral(cluster_label / 10.),
                     fontdict={'family': 'Arial', 'size': 10})
    else:
        for x, y, name, cluster_label in zip(x1, x2, sample_names, target_ints):
            ax1.text(x, y, name, ha='center', va="center",
                     color=plt.cm.spectral(cluster_label / 10.),
                     fontdict={'family': 'Arial', 'size': 10})

    try:
        # now loadings on twin axis:
        if loadings.any():
            ax2 = ax1.twinx().twiny()
            l1, l2 = loadings[:,0], loadings[:,1]
            ax2.scatter(l1, l2, 100, edgecolors='none', facecolors='none');
            for x, y, l in zip(l1, l2, feature_names):
                ax2.text(x, y, l ,ha='center', va="center", size=8, color="darkgrey",
                    fontdict={'family': 'Arial', 'size': 9})
            ax2.set_xticklabels([])
            ax2.set_xticks([])
            ax2.set_yticklabels([])
            ax2.set_yticks([])
    except:
        pass

    # control aesthetics:
    ax1.set_xlabel('')
    ax1.set_ylabel('')
    ax1.set_xticklabels([])
    ax1.set_xticks([])
    ax1.set_yticklabels([])
    ax1.set_yticks([])

    sns.plt.savefig(outputfile, bbox_inches=0)
    plt.clf()
    return

def scatterplot_2d_bokeh(X, sample_names, target_ints=None, target_idx=None,
                   outputfile=std_output_path+'2d_bokeh.html', nb_clusters=0): 
    if X.shape[1] != 2:
        raise ValueError('Only two-dimensional matrices are supported')

    output_file(outputfile)
    TOOLS="pan,wheel_zoom,reset,hover,box_select,save"
    p = figure(tools=TOOLS,
               plot_width=800, title_text_font="Arial", 
               plot_height=600, outline_line_color="white")

    if nb_clusters:
        cl = AgglomerativeClustering(linkage='ward', affinity='euclidean', n_clusters=nb_clusters)
        clusters = cl.fit_predict(X)
        # get color palette:
        colors = sns.color_palette('husl', n_colors=nb_clusters)
        colors = [tuple([c * 256 for c in color]) for color in colors]
        colors = ['#%02x%02x%02x' % colors[i] for i in clusters]
    else:
        colors = sns.color_palette('husl', n_colors=len(target_idx))
        colors = [tuple([c * 256 for c in color]) for color in colors]
        colors = ['#%02x%02x%02x' % colors[i] for i in clusters]

    source = ColumnDataSource(data=dict(x=X[:,0], y=X[:,1], name=sample_names))

    p.circle(x=X[:,0], y=X[:,1],
             source=source, size=8, color=colors,
             fill_alpha=0.9, line_color=None)

    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("name", "@name")]
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_label_text_font_size = '0pt'
    p.axis.major_tick_line_color = None
    p.axis[0].ticker.num_minor_ticks = 0
    p.axis[1].ticker.num_minor_ticks = 0
    save(p)


def scatterplot_3d(X, sample_names, target_ints=None, target_idx=None, loadings=None,
                   outputfile=std_output_path+'3d.pdf', nb_clusters=0):
    
    sns.set_style('white')
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x1, x2, x3 = X[:,0], X[:,1], X[:,2]
    if nb_clusters:
        clustering = AgglomerativeClustering(linkage='ward', affinity='euclidean', n_clusters=nb_clusters)
        clustering.fit(X)
        # empty first:
        for x, y, z in zip(x1, x2, x3):
            ax.scatter(x, y, z, edgecolors='none', facecolors='none')
        # add slice names:
        for x, y, z, name, cluster_label in zip(x1, x2, x3, sample_names, clustering.labels_):
            ax.text(x, y, z, name, ha='center', va="center",
                     color=plt.cm.spectral(cluster_label / 10.),
                     fontdict={'family': 'Arial', 'size': 7})
    else:
        for x, y, z in zip(x1, x2, x3):
            ax.scatter(x, y, z, edgecolors='none', facecolors='none')
        for x, y, z, name, cluster_label in zip(x1, x2, x3, sample_names, target_ints):
            ax.text(x, y, z, name, ha='center', va="center",
                     color=plt.cm.spectral(cluster_label / 10.),
                     fontdict={'family': 'Arial', 'size': 10})

    plt.savefig(outputfile, bbox_inches=0)
    plt.clf()

def color_plt_labels(ax, target_ints=None, fontsize=5):
    # xlabels:
    for idx, label in enumerate(ax.get_xticklabels()):
        label.set_rotation('vertical')
        label.set_fontname('Arial')
        label.set_fontsize(fontsize)
        if target_ints:
            label.set_color(plt.cm.spectral(target_ints[idx] / 10.))

    # ylabels:
    for idx, label in enumerate(ax.get_yticklabels()):
        label.set_rotation('horizontal')
        label.set_fontname('Arial')
        label.set_fontsize(fontsize)
        if target_ints:
            label.set_color(plt.cm.spectral(target_ints[-idx-1] / 10.)) # watch out: different indexing both axis


def clustermap(X, sample_names, target_ints=None, target_idx=None,
               outputfile=std_output_path+'clustermap.pdf', fontsize=5):
    # convert to pandas dataframe:
    df = pd.DataFrame(data=X, columns=(sample_names))
    df = df.applymap(lambda x:int(x*1000)).corr()

    # clustermap plotting:
    cm = sns.clustermap(df)
    ax = cm.ax_heatmap
    color_plt_labels(ax, target_ints, fontsize=fontsize)

    cm.savefig(outputfile)
    plt.clf()

def scipy_dendrogram(cluster_tree, sample_names, target_ints=None, target_idx=None,
               outputfile=std_output_path+'scipy_dendrogram.pdf', fontsize=5):
    cluster_tree.dendrogram.draw_scipy_tree(labels=sample_names,
                                            target_ints=target_ints,
                                            target_idx=target_idx)

def ete_dendrogram(cluster_tree, sample_names, target_ints=None, target_idx=None,
                   outputfile=std_output_path+'ete_dendrogram.pdf',
                   fontsize=5, save_newick=True):
    dendrogram = cluster_tree.dendrogram.draw_ete_tree(labels=sample_names,
                                                       target_ints=target_ints,
                                                       target_idx=target_idx)
    


