---
layout: page
title: The MHC region
---

The MHC (major histocompatiblity complex) is a region on chromosome 6 in the human genome. It is enriched for  genes of the immune system, including the HLA (human leukocyte antigen) genes. Unlike antibodies and T-cell receptors, the HLA genes do not undergo somatic hypermutation or genomic rearrangement to achieve high diversity. However, they do display antigen to antibodies and T-cell receptors, so they are still considered part of the adaptive immune system. Accordingly, they still benefit from high genomic diversity, similarly to antibodies and T-cell receptors; any haplotype that becomes too common is susceptible to epidemic if a disease agent evolves the capacity to evade it. Since the MHC lacks the capacity for genomic rearrangement, it must rely on natural selection to achieve diversity, and is thusly under intense diversifying selection. For this reason, the MHC region is one of the most wildly polymorphic regions of the human genome. Moreover, it is enriched for complex structural variation as well as point variants.

Because the MHC region is so polymorphic, it is one of the regions of the human genome that is not well-served by linear references. Recognizing this limitation, starting with with GRCh38 the Genome Reference Consortium (GRC) began distributing a set of alternate scaffolds for the MHC (and some other regions) along with the reference sequence. However, many genomics tools do not yet support these alternate scaffolds well. 

<br/>

## Constructing an MHC graph

Graph genome tools offer one possibility for how we could use the alternate scaffolds. The first step is to build a graph. You have a few options for how you might accomplish this. The most obvious way is probably an alignment method. You have already seen `seqwish`, `vg msga`, and `minigraph`, which provide several different methods to build graphs from sequences. 

### MSA based variation graphs

However, you may also want to use a different MSA tool. `vg` has a method to construct a graph directly from a multiple sequence alignment in either MAF or Clustal format. The following example shows how you could do this using Clustal Omega.

    # use Clustal Omega to make a multiple sequence alignment
    clustalo -i sequences.fasta --outfmt clustal > mult_seq_aln.clustal
    
    # convert the multiple sequence alignment to a VG file
    # -M = input file, -F = format, -m = max node size
    vg construct -M mult_seq_aln.clustal -F clustal -m 32 > msa.vg

You are free to try this method, but be warned that the MHC region is large and it may overwhelm MSA tools that were designed for smaller sequences. If you are interested, you might want to try making an MSA graph from other sequences as well (e.g. the HIV sequences from two days ago).

It should be noted that there are other methods that you could use to build a graph of the MHC region. For instance, you could find a VCF and use `vg construct -v`. You could use an assembly tool to build an assembly graph and construct a VG from the GFA file.

<br/>

## MHC typing using variation graphs

An interesting question to ask for a new sample is which MHC scaffold (or pair of scaffolds) will represent its MHC region best. In reality, any individual's MHC haplotypes are unlikely to match any of the MHC scaffolds well. However, they will have recombinant subsequences in common with the scaffolds. Moreover, previous studies have demonstrated benefits in downstream application for choosing more representative sequences for the reference, even if these sequences are imperfect (see Dilthey, et al. 2014). 

We have provided for you a set of sequencing reads from the Human Genome Structural Variation Consortium in the path `/media/gtpb_shared_drive/To_Participant/MHC/TrioData`. They come from a parent-child: the Han Chinese trio HG00512-HG00513-HG00514. The highest-numbered sample is the child. You will have both Illumina paired end short reads and PacBio long reads. Rather than providing the entire genomic dataset, we have extracted reads that mapped to the MHC region or one of the alternate scaffolds using a conventional read mapper. Of course, that means that these datasets are already biased by mapping to a linear reference. However, the volume of data for a full genomic dataset is probably too computationally demanding for an exercise in this environment.

We have also provided you a different set of reds for the individual HG002 in the path `/media/gtpb_shared_drive/To_Participant/MHC/HG002`. This folder contains CCS reads and ultralong ONT reads for the MHC region of this individual. The reads are split by haplotype using trio binning and phasing. The files `*.H1.*` contains reads from the first haplotype, `*.H2.*` from the second haplotype and `*.untagged.*` contains reads which could not be confidently assigned to a haplotype.

The reference alles for each HLA gene are in `/media/gtpb_shared_drive/To_Participant/MHC/IMGT_alleles`. The alleles are grouped per gene, containing either genomice sequence (`*_gen.fasta`), coding sequences (`*_nuc.fasta`) and protein sequences (`*_prot.fasta`).
Use these to establish HLA genotypes for each genome.

The GRCh38 ALTs (alternative haplotypes) for the MHC are provided in `/media/gtpb_shared_drive/To_Participant/MHC/MHC.fa.gz`.
These can be used as the basis for a reference model of the MHC.

<br/>

## Variant calling in VG

In order to choose an MHC scaffold, it might be useful to perform variant calling against the graph you construct. However, this is not the only route forward. Think about how you would use the results before you devote too much time to it. Note that to output a VCF, you will need to have constructed your graph using a method that preserved the reference sequence as a path. 

    vg construct -r small/x.fa -v small/x.vcf.gz >x.vg
	vg index -x x.xg -g x.gcsa -k 16 x.vg
	vg map -d x -G <(vg sim -n 1000 -e 0.01 -i 0.005 -l 50 -a -x x.xg) >aln.gam

augment the novel alleles into the graph to genotype

	vg augment x.vg aln.gam -A aln.aug.gam >x.aug.vg
	vg index -x x.aug.xg x.aug.vg
	vg pack -x x.aug.xg -g aln.aug.gam -o aln.aug.gam.pack
	vg call x.aug.xg -k aln.aug.gam.pack -s rando >rando.vcf

How could you use these variant calls to determine which MHC scaffold(s) are most appropriate for this sample? Since you have trio datasets may be interesting to look at Mendelian consistency in your approach.

<br/>

## Back

Back to [main page](../index.md).
