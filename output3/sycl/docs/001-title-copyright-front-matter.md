![](images/d91b12d657fe02f83bf6214177f72ca5d5079f5d5af6aebae0c9cd2aaf8f618f.jpg)

SYCL TM

Data Parallel C++

Programming Accelerated Systems Using C++ and SYCL

Second Edition

James Reinders Ben Ashbaugh James Brodman Michael Kinsner John Pennycook Xinmin Tian

Foreword by Erik Lindahl, GROMACS and Stockholm University

# Data Parallel C++

# Programming Accelerated Systems Using C++ and SYCL

Second Edition

James Reinders

Ben Ashbaugh

James Brodman

Michael Kinsner

John Pennycook

Xinmin Tian

Foreword by Erik Lindahl, GROMACS and Stockholm University

## Data Parallel C++: Programming Accelerated Systems Using C++ and SYCL, Second Edition

James Reinders Beaverton, OR, USA Ben Ashbaugh Folsom, CA, USA James Brodman Marlborough, MA, USA

Michael Kinsner Halifax, NS, Canada John Pennycook San Jose, CA, USA Xinmin Tian Fremont, CA, USA

ISBN-13 (pbk): 978-1-4842-9690-5 https://doi.org/10.1007/978-1-4842-9691-2

ISBN-13 (electronic): 978-1-4842-9691-2

## Copyright © 2023 by Intel Corporation

This work is subject to copyright. All rights are reserved by the Publisher, whether the whole or part of the material is concerned, specifically the rights of translation, reprinting, reuse of illustrations, recitation, broadcasting, reproduction on microfilms or in any other physical way, and transmission or information storage and retrieval, electronic adaptation, computer software, or by similar or dissimilar methodology now known or hereafter developed.

![](images/c3535ad0fdc9a2663cff9ec993b4a137583d99315a7d3a54ad22545b2d62e4d4.jpg)

Open Access This book is licensed under the terms of the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate

credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if change were made.

The images or other third party material in this book are included in the book’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the book's Creative Commons license and vour intendec use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.

Trademarked names, logos, and images may appear in this book. Rather than use a trademark symbol with every occurrence of a trademarked name, logo, or image we use the names, logos, and images only in an editorial fashion and to the benefit of the trademark owner, with no intention of infringement of the trademark.

The use in this publication of trade names, trademarks, service marks, and similar terms, even if they are not identified as such, is not to be taken as an expression of opinion as to whether or not they are subject to proprietary rights.

Intel, the Intel logo, Intel Optane, and Xeon are trademarks of Intel Corporation in the U.S. and/or other countries. OpenCL and the OpenCL logo are trademarks of Apple Inc. in the U.S. and/or other countries. OpenMP and the OpenMP logo are trademarks of the OpenMP Architecture Review Board in the U.S, and/or other countries, SYCL. the SYCL logo. Khronos and the Khronos Group logo are trademarks of the Khronos Group Inc. The open source DPC++ compiler is based on a published Khronos SYCL specification. The current conformance status of SYCL implementations can be found at https://www.khronos org/conformance/adopters/conformant-products/sycl.

Software and workloads used in performance tests may have been optimized for performance only on Intel microprocessors Performance tests are measured using specific computer systems, components, software, operations and functions. Any change to any of those factors may cause the results to vary. You should consult other information and performance tests to assist you in fully evaluating your contemplated purchases, including the performance of that product when combined with other products. For more complete information visit https://www.intel.com/benchmarks. Performance results are based on testing as of dates shown in configuration and may not reflect all publicly available security updates. See configuration disclosure for details. No product or component can be absolutely secure. Intel technologies' features and benefits depend on system configuration and may require enabled hardware, software or service activation. Performance varies depending on system configuration. No computer system can be absolutely secure. Check with vour system manufacturer or retailer or learn more at www.intel.com.

While the advice and information in this book are believed to be true and accurate at the date of publication, neither the authors nor the editors nor the publisher can accept any legal responsibility for any errors or omissions that may be made. The publisher makes no warranty, express or implied, with respect to the material contained herein.

Managing Director, Apress Media LLC: Welmoed Spah

Acquisitions Editor: Susan McDermot

Development Editor: James Markham

Coordinating Editor: Jessica Vakili

Distributed to the book trade worldwide by Springer Science+Business Media New York, 1 NY Plaza, New York, NY 10004. Phone 1-800-SPRINGER, fax (201) 348-4505, e-mail orders-ny@springer-sbm.com, or visit https://www.springeronline.com. Apress Media, LLC is a California LLC and the sole member (owner) is Springer Science + Business Media Finance Inc (SSBM Finance Inc). SSBM Finance Inc is a Delaware corporation.

For information on translations, please e-mail booktranslations@springernature.com; for reprint, paperback, or audio rights, please e-mail bookpermissions@springernature.com.

Apress titles may be purchased in bulk for academic, corporate, or promotional use. eBook versions and licenses are also available for most titles. For more information, reference our Print and eBook Bulk Sales web page at https://www.apress.com bulk-sales.

Any source code or other supplementary material referenced by the author in this book is available to readers on the Github repository: https://github.com/Apress/Data-Parallel-CPP. For more detailed information, please visit https://www.apress. com/gp/services/source-code.

Paper in this product is recyclable
